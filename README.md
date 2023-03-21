# MongoMultiVendor

This project is intended to be a starting point for a multi-vendor platform. The backend consists of a few models. 

## Sessions

There is a sessions module for loading (user, organization, and account) from a flask session. This module offers a decorator for loading each of the previously mentioned models from a user's session. example: account_loader wraps a

## Graphql

Graphene can get a little messy to work with when your building a lot of mutations so there is a graphql module in this package that inspired by flask-admin. It allows you to quickly create the graphql crud operations for your mongoengine models with minimal code.
