from bcrypt import checkpw
from flask import session
from re import compile, IGNORECASE
from time import time
from .status import STATUS_STATES
from .fields import PasswordField, PhoneNumberField
from ..media.base import Media
from flask import request, session
from uuid import uuid4
from bson import ObjectId
from datetime import datetime
from ..document import FMADocumentMetaclass
from mongoengine import (
  GenericReferenceField,
  queryset_manager,
  DateTimeField,
  BooleanField,
  StringField,
  EmailField,
  IntField,
  ReferenceField,
  ListField,
  DENY,
  PULL,
  NULLIFY,
  CASCADE,
  PointField,
  EmbeddedDocument,
  EmbeddedDocumentField,
  Document
)
from ..sessions import (
  current_user, 
  Users,
  user_loader, 
  user_loaded
)


@user_loader
def load_user():
  USER_ID_SESSION_KEY = Users.USER_ID_KEY
  if user:=getattr(request, USER_ID_SESSION_KEY, None):
    return user
  if USER_ID_SESSION_KEY in session: 
    user_id = ObjectId(session[USER_ID_SESSION_KEY])
    user = User.objects.get(id=user_id)
    if user.status == "active":
      setattr(request, USER_ID_SESSION_KEY, user)
      return user
    else:
      [session.pop(key) for key in list(session.keys())]
      raise Exception(f"Your account status has been set to ({user.status})")


"""USER MODELS"""

class Permission(Document, metaclass=FMADocumentMetaclass):
  meta = {
    "collection": "account_permissions",
    "allow_inheritance": True
  }
  action = StringField(min_length=5, max_length=80, null=False, unique_with="_cls")
  description = StringField(max_length=1000, null=True)

  def clean(self):
    self.action = self.action.strip().replace(" ", "_").lower()

  @queryset_manager
  @user_loaded
  def secured_objects(cls, qs):
    return qs

  def __str__(self):
    if self.description:
      return self.description
    return self.action

class UserPermission(Permission):
  pass

class BaseRole(Document, metaclass=FMADocumentMetaclass):
  meta = {
    "collection": "account_roles",
    "allow_inheritance": True
  }
  name = StringField(max_length=80)
  created = DateTimeField(default=datetime.utcnow)
  is_admin = BooleanField(default=False)
  default = BooleanField(default=False)

  def __str__(self):
    return self.name

  @queryset_manager
  @user_loaded
  def secured_objects(cls, qs):
    name = cls.__snakename__
    if current_user.has_permission(f"{name}.read"):
      return qs
    else:
      return qs(id=current_user.role.id)

  @classmethod
  def get_default_role(cls):
    role = cls.objects.filter(default=True).first()
    if role:
      return role
    role = cls(
      name="default",
      permissions=[],
      is_admin=False,
      default=True
    )
    role.save()
    return role

  @property
  def permission_class(self):
    return self.__class__.permissions.field.document_type

  def has_permission(self, action):
    # print(f"\033[92m {self.__class__.__name__} {action} \033[0m")
    if self.is_admin:
      return True
    if " " in action:
      raise Exception(f'permissions do not contain open space ({action})')
    else:
      test_item = lambda item: item.action == action
      return next(filter(test_item, self.permissions), None)

  def assert_permission(self, action):
    access = self.has_permission(action)
    if not access:
      try:
        perm = self.permission_class.objects.get(action=action)
      except:
        self.permission_class(action=action)
      msg = f"Permission denied: {perm.description or perm.action}"
      raise Exception(msg)

  def clean(self):
    if changes := getattr(self, '_changed_fields', None):
      if 'default' in changes and self.defaut:
        self.__class__.objects.filter(
          default=True).update(
            set__default=False)

  def __str__(self):
    return self.name

class UserRole(BaseRole):
  permissions = ListField(
    ReferenceField(UserPermission), 
    default=[]
  )

class BaseGroup(Document, metaclass=FMADocumentMetaclass):
  meta = {
    "collection": "account_groups",
    "allow_inheritance": True,
    "indexes": [
      {"fields": ["name", "_cls"], "unique": True}
    ]
  }
  name = StringField(required=True, min_length=1, max_length=255)
  active = BooleanField(default=True)
  created = DateTimeField(default=datetime.utcnow)

  def __str__(self):
    return self.name
  
  @queryset_manager
  @user_loaded
  def secured_objects(cls, qs):
    name = cls.__snakename__
    if current_user.has_permission(f"{name}.read"):
      return qs
    else:
      return qs(id__in=current_user.groups)

class UserGroup(BaseGroup):
  name = StringField(required=True, min_length=1, max_length=255)
  active = BooleanField(default=True)
  created = DateTimeField(default=datetime.utcnow)

class BaseUser(Document, metaclass=FMADocumentMetaclass):
  # can be subclasses for oauth or other things
  meta = {
    "allow_inheritance": True,
    "collection": "account_users"
  }
  phone_number = PhoneNumberField()
  email = EmailField(
    null=False,
    required=True,
    unique=True, 
    max_length=255
  )
  email_verified = BooleanField(
    default=False
  )
  created = DateTimeField(
    default=datetime.utcnow, 
    null=False
  )
  updated = DateTimeField(
    default=datetime.utcnow, 
    null=False
  )
  role = ReferenceField(
    BaseRole, 
    reverse_delete_rule=DENY,
    default=BaseRole.get_default_role,
    null=False
  )

  @queryset_manager
  @user_loaded
  def secured_objects(cls, qs):
    name = cls.__snakename__
    if current_user.has_permission(f"{name}.read"):
      return qs
    else:
      return qs(id=current_user.id)

class Address(EmbeddedDocument):

  line_1 = StringField(max_length=255, required=True, null=True)
  line_2 = StringField(max_length=255, required=True, null=True)
  city = StringField(max_length=255, required=True, null=True)
  state = StringField(max_length=255, required=True, null=True)
  postal_code = StringField(max_length=255, required=True, null=True)
  country = StringField(max_length=255, required=True, null=True)
  default = BooleanField(default=False)
  coordinates = PointField(null=False)

class User(BaseUser):
  meta = {
    "indexes": ["groups"]
  }
  avatar = ReferenceField(
    Media, 
    null=True, 
    reverse_delete_rule=NULLIFY
  )
  email = EmailField(
    null=False,
    required=True,
    unique=True, 
    max_length=255
  )
  email_verified = BooleanField(
    default=False
  )
  password = PasswordField(
    null=False,
  )
  first_name = StringField(
    max_length=255
  )
  last_name = StringField(
    max_length=255
  )
  addresses = ListField(
    EmbeddedDocumentField(Address),
    default=[]
  )
  created = DateTimeField(
    default=datetime.utcnow, 
    null=False
  )
  status = StringField(
    default="active",
    choices=STATUS_STATES
  )
  role = ReferenceField(
    UserRole, 
    reverse_delete_rule=DENY,
    default=UserRole.get_default_role,
    null=False
  )
  groups = ListField(
    ReferenceField(
      UserGroup
    ),
    default=[],
    reverse_delete_rule=PULL
  )

  def __str__(self):
    return f"{self.email} ({self.status})"


  def clean(self):
    if changes := getattr(self, '_changed_fields', None):
      if "password" in changes and \
        current_user.id != self.id:
        raise Exception("You cannot change another user's password")
      if "role" in changes:
        if not current_user.has_permission('user.assign_role'):
          raise Exception("You do not have permission to assign a user's role")
      if "status" in changes:
        if not current_user.has_permission('user.set_status'):
          raise Exception("You do not have permission to set a user's status")


  auth_lookup_fields = ["email"]

  @classmethod
  def search_by_identifier(cls, lookup_value):
    query = {
      "$or": [
        {field: { '$regex': compile(f"^{lookup_value}$", IGNORECASE)}} \
        for field in cls.auth_lookup_fields
      ]
    }
    return cls.objects.filter(__raw__=query).first()
    

  @classmethod
  def authenticate(cls, lookup_value, password):
    user = cls.search_by_identifier(lookup_value)
    assert user is not None, \
      'Invalid email/password combo'
    password_match = checkpw(
      password.encode('utf-8'), 
      user.password
    )
    assert password_match is not None, \
      'Invalid email/password combo'
    assert user.status == 'active', \
      "Your account is not active"
    session['user'] = str(user.id)
    return user

  @classmethod
  def logout(cls):
    session.clear()

  @property
  def has_permission(self):
    return self.role.has_permission

  @property
  def assert_permission(self):
    return self.role.assert_permission

class PasswordResetCode(Document):
  meta = {
    "collection": "account_password_reset",
    "indexes": [
      {
        'fields': ['created'],
        'expireAfterSeconds': 60
      }
    ]
  }
  user = ReferenceField(BaseUser, unique=True, required=True)
  code = StringField(default=lambda:str(uuid4()), null=False)
  created = DateTimeField(default=datetime.utcnow(), null=False)
  attempts = IntField(default=0)

class UserAccess(Document):

  meta = {
    "collection": "account_access",
    "indexes": ["user"]
  }
  user = ReferenceField(User, required=True, null=False)
  resource = GenericReferenceField(required=True)
  created = DateTimeField()
