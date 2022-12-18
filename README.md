# MongoMultiVendor

This project is intended to be a starting point for a multi-vendor platform. The backend consists of a few models. 
## Users

###### Models

* BaseUser - Document
  - phone_number = PhoneNumberField (Custom field subclassed from StringField)
  - email = EmailField
  - email_verified = BooleanField
  - created = DateTimeField
  - updated = DateTimeField
  - role = ReferenceField(BaseRole)

* User(BaseUser) - Document
  - avatar = ReferenceField(Media)
  - email = EmailField
  - email_verified = BooleanField
  - password = PasswordField
  - first_name = StringField
  - last_name = StringField
  - addresses = ListField(Address)
      - line_1 = StringField
      - line_2 = StringField
      - city = StringField
      - state = StringField
      - postal_code = StringField
      - country = StringField
      - default = BooleanField
      - coordinates = PointField
  - created = DateTimeField
  - status = StringField
  - role = ReferenceField(UserRole)
  - groups = ListField(UserGroup)

* PasswordResetCode - Document
  - user = ReferenceField(BaseUser)
  - code = StringField
  - created = DateTimeField
  - attempts = IntField
 
* BasePermission - Document
  - action = StringField
  - description = StringField
 
* UserPermission(BasePermission) - Document
  - action = StringField
  - description = StringField

* BaseRole - Document
  - name = StringField
  - created = DateTimeField
  - is_admin = BooleanField
  - default = BooleanField
 
* UserRole(BaseRole) - Document
  - name = StringField
  - created = DateTimeField
  - is_admin = BooleanField
  - default = BooleanField
  - permissions = ListField(UserPermission)
 
* Group - Document
  - name = StringField
  - active = BooleanField
  - created = DateTimeField

## Organizations

###### Models


* Organization - Document
  logo = ReferenceField(Media)
  name = StringField
  require_account_approval = BooleanField
  status = StringField
  payment_processors = ListField(
    GenericEmbeddedDocumentField(
      choices=(Square,)
    ),
  )
  is_public = BooleanField(default=True)
  updated = DateTimeField(default=datetime.utcnow, null=False)
  created = DateTimeField(default=datetime.utcnow, null=False)

* OrganizationLocation - Document
  - addresses = ListField(Address)
      - line_1 = StringField
      - line_2 = StringField
      - city = StringField
      - state = StringField
      - postal_code = StringField
      - country = StringField
      - default = BooleanField
      - coordinates = PointField
  - organization = ReferenceField(Organization)
  - is_public = BooleanField
  - location_name = StringField
  - business_hours = EmbeddedDocumentField(BusinessHours)
  - updated = DateTimeField(default=datetime.utcnow, null=False)
  - created = DateTimeField(default=datetime.utcnow, null=False)
  - metadata = DictField()

* AccountPermission(Permission) - Document
  - action = StringField
  - description = StringField

* AccountRole(BaseRole) - Document
  - name = StringField
  - created = DateTimeField
  - is_admin = BooleanField
  - default = BooleanField
  - permissions = ListField(UserPermission)
  - organization = ReferenceField(Organization)

* AccountGroup(BaseGroup) - Document
  - organization = ReferenceField(Organization)
  - name = StringField
  - active = BooleanField
  - created = DateTimeField

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


## Sessions

There is a sessions module for loading (user, organization, and account) from a flask session. This module offers a decorator for loading each of the previously mentioned models from a user's session. example: account_loader wraps a

## Graphql

Graphene can get a little messy to work with when your building a lot of mutations so there is a graphql module in this package that inspired by flask-admin. It allows you to quickly create the graphql crud operations for your mongoengine models with minimal code.

## Payments

Each user goes into a main user pool, outside of the bounds of any one organization which allows for users to sign up once and join any organization without going through the registration process a second time.
