# MongoMultiVendor

This project is intended to be a starting point for a multi-vendor platform. The backend consists of a few models. 
## Users

###### Models

* BaseUser: Base User model (mixin of User Object) - Document
  - phone_number = PhoneNumberField (Custom field subclassed from StringField)
  - email = EmailField
  - email_verified = BooleanField
  - created = DateTimeField
  - updated = DateTimeField
  - role = ReferenceField(BaseRole)

* User: - Document (subclassed from Base User)
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
  - status = StringField(default="active")
  - role = ReferenceField(UserRole)
  - groups = ListField(UserGroup)

* PasswordResetCode: Document
  - user = ReferenceField(BaseUser)
  - code = StringField
  - created = DateTimeField
  - attempts = IntField
 
* BasePermission: Document
  - name = StringField(max_length=80)
  - created = DateTimeField(default=datetime.utcnow)
  - is_admin = BooleanField(default=False)
  - default = BooleanField(default=False)
 
* UserPermission: Document
  - name = StringField(max_length=80)
  - created = DateTimeField(default=datetime.utcnow)
  - is_admin = BooleanField(default=False)
  - default = BooleanField(default=False)
  - permissions = ListField(UserPermission)

* BaseRole: Document
  - name = StringField(max_length=80)
  - created = DateTimeField(default=datetime.utcnow)
  - is_admin = BooleanField(default=False)
  - default = BooleanField(default=False)
 
* UserRole: Document (subclassed from BaseRole)
  - name = StringField(max_length=80)
  - created = DateTimeField(default=datetime.utcnow)
  - is_admin = BooleanField(default=False)
  - default = BooleanField(default=False)
  - permissions = ListField(UserPermission)
 
* Group: Documument
  - name = StringField(required=True, min_length=1, max_length=255)
  - active = BooleanField(default=True)
  - created = DateTimeField(default=datetime.utcnow)

## Organizations

###### Models

* Organization: a single business or organization
* Account: a single user membership to a organization, consists of a few notable references:
 - user
 - organization
 - role

## Sessions

There is a sessions module for loading (user, organization, and account) from a flask session. This module offers a decorator for loading each of the previously mentioned models from a user's session. example: account_loader wraps a

## Graphql

Graphene can get a little messy to work with when your building a lot of mutations so there is a graphql module in this package that inspired by flask-admin. It allows you to quickly create the graphql crud operations for your mongoengine models with minimal code.

## Payments

Each user goes into a main user pool, outside of the bounds of any one organization which allows for users to sign up once and join any organization without going through the registration process a second time.
