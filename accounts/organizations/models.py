from time import time
from ..sessions import (
  user_loaded,
  current_user
)
from ..users import (
  BaseUser, 
  BaseRole, 
  BaseGroup, 
  Permission, 
  Address,
)
from ..document import FMADocumentMetaclass
from ..users.status import STATUS_STATES
from ..users.fields import MilitaryTimeField, PhoneNumberField
from time import time
from ..media import Media
from datetime import datetime
from mongoengine import (
  Q,
  DictField,
  queryset_manager,
  BooleanField,
  ListField,
  ReferenceField,
  PULL,
  CASCADE,
  DENY,
  StringField,
  EmailField,
  ReferenceField,
  EmbeddedDocumentField,
  EmbeddedDocument,
  GenericEmbeddedDocumentField,
  DateTimeField,
  NULLIFY,
  Document
)


class Organization(Document, metaclass=FMADocumentMetaclass):

  meta = {
    "collection": "account_organizations",
    "indexes": ['is_public']
  }
  logo = ReferenceField(Media, null=True, reverse_delete_rule=NULLIFY)
  name = StringField(
    unique=True, 
    required=True, 
    min_length=2, 
    max_length=255
  )
  require_account_approval = BooleanField(
    default=True
  )
  status = StringField(
    default="active",
    choices=STATUS_STATES
  )
  payment_processors = ListField(
    GenericEmbeddedDocumentField(
      # choices=(Square,)
    ),
    default=[]
  )
  is_public = BooleanField(default=True)
  updated = DateTimeField(default=datetime.utcnow, null=False)
  created = DateTimeField(default=datetime.utcnow, null=False)

  def clean(self):
    if self.logo:
      if "image" not in self.logo.content_type:
        self.logo = None

  def __str__(self):
    return self.name

  def get_default_admin_role(self):
    role = AccountRole.objects.filter(
      organization=None,
      is_admin=True).first()
    if not role:
      role = AccountRole(
        name="Administrator",
        is_admin=True,
        default = False
      )
      role.save()
    return role
  
  @user_loaded
  def save(self, *args, **kwargs):
    if self.pk is None:
      assert current_user.has_permission('organization.create'), \
        "You dont have permission to create a organization record"
      super(self.__class__, self).save(*args, **kwargs)
      account = Account(
        organization=self,
        user = current_user.id,
        role = self.get_default_admin_role()
      )
      account.save()
    return super(self.__class__, self).save(*args, **kwargs)

  @queryset_manager
  def secured_objects(cls, qs):
    name = cls.__snakename__
    if current_user:
      if current_user.has_permission(f"{name}.read"):
        return qs
      else:
        orgs = Account.objects(
          user=current_user.id
          ).distinct('organization')
        return qs(Q(public=True) | Q(organization__in=orgs))
    else:
      return qs(public=True)

class BusinessDay(EmbeddedDocument):

  open_time = MilitaryTimeField(required=True)
  close_time = MilitaryTimeField(required=True)

class BusinessHours(EmbeddedDocument):

  sunday = EmbeddedDocumentField(BusinessDay, null=True)
  monday = EmbeddedDocumentField(BusinessDay, null=True)
  tuesday = EmbeddedDocumentField(BusinessDay, null=True)
  wednesday = EmbeddedDocumentField(BusinessDay, null=True)
  thursday = EmbeddedDocumentField(BusinessDay, null=True)
  friday = EmbeddedDocumentField(BusinessDay, null=True)
  saturday = EmbeddedDocumentField(BusinessDay, null=True)

class OrganizationLocation(Document):
  meta = {"collection": "account_business_locations"}
  organization = ReferenceField(Organization, required=True, reverse_delete_rule=CASCADE)
  location_name = StringField(null=True, max_length=80)
  business_email = EmailField()
  phone_number = PhoneNumberField()
  address = EmbeddedDocumentField(Address, required=True)
  is_public = BooleanField(default=True)
  business_hours = EmbeddedDocumentField(BusinessHours)
  updated = DateTimeField(default=datetime.utcnow, null=False)
  created = DateTimeField(default=datetime.utcnow, null=False)
  metadata = DictField()

  @queryset_manager
  def secured_objects(cls, qs):
    return qs(is_public=True)
  
class AccountPermission(Permission):
  pass

class AccountRole(BaseRole):
  meta = {
    "indexes": [
      {'fields': ['_cls', 'name', 'organization'], "unique": True}
    ]
  }
  permissions = ListField(
    ReferenceField(AccountPermission), 
    default=[]
  )
  organization = ReferenceField(
    Organization,
    null=True
  )


class AccountGroup(BaseGroup):
  meta = {
    "indexes": [
      {"fields": ["_cls", "name", "organization"], "unique": True}
    ]
  }
  organization = ReferenceField(
    Organization,
    null=True
  )

class Account(Document, metaclass=FMADocumentMetaclass):
  meta = {
    "collection": "account_accounts",
    "allow_inheritance": True,
    "indexes": [
      {"fields": ['user', 'organization'], "unique": True},
      {"fields": ["groups", "organization"]}
    ]
  }
  user = ReferenceField(
    BaseUser,
    reverse_delete_rule=CASCADE,
    required=True
  )
  role = ReferenceField(
    "AccountRole",
    reverse_delete_rule=DENY,
    default=lambda:AccountRole.get_default_role()
  )
  organization = ReferenceField(
    Organization,
    reverse_delete_rule = CASCADE
  )
  groups = ListField(
    ReferenceField(
      "AccountGroup",
      reverse_delete_rule=PULL
    )
  )
  status = StringField(
    default="active",
    choices=STATUS_STATES
  )
  created = DateTimeField(
    default=datetime.utcnow, 
    required=True
  )

  def __str__(self):
    return f"{self.user.email} {self.organization}"

  @property
  def has_permission(self, name):
    if self.role.has_permission(name):
      return True
    else:
      split = name.split('.')
      admin_permission = f"{split[0]}.admin_{split[1]}"
      if self.user.role.has_permission(admin_permission):
        return True
    return False

  @queryset_manager
  @user_loaded
  def secured_objects(cls, qs):
    name = cls.__snakename__
    if current_user.has_permission(f"{name}.read"):
      return qs
    else:
      return qs(user=current_user.id)

