# MongoMultiVendor

This project is intended to be a starting point for a multi-vendor platform. The backend consists of a few models. 
## Users

###### Models

* BaseUser: Base User model (subclassed by User)
  phone_number = PhoneNumberField (Custom field subclassed from StringField)
  email = EmailField
  email_verified = BooleanField
  created = DateTimeField
  updated = DateTimeField
  role = ReferenceField(BaseRole)

* User: a user of this platform
  - 
* Role: attatched to a user/account and lists the permissions
* Permission: single persmission entry
  - action: name of action ie: "user_role.read"
  - description: short description of action
* Group: used to group users

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
