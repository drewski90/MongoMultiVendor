# MongoMultiVendor

This project is intended to be a starting point for a multi-vendor platform. The backend consists of a few models. 
## Users

* User: a user of this platform
* Role: attatched to a user/account and lists the permissions
* Group: used to group users

## Organizations

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
