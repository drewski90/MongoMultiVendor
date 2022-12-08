from ...graphql import GQLModelSchema, ObjectId
from ...sessions import (
  current_user, 
  user_loaded, 
  current_account
)
from flask import session
from graphene import (
  Field,
  Mutation
)

from ..models import (
  Organization,
  Account,
  AccountGroup,
  AccountRole,
  BusinessAddress
)
from .types import (
  OrganizationType,
  AccountRoleType,
  AccountType,
  AccountGroupType,
  BusinessAddressType
)


class AccountAccessMixin:

  def is_accessible(view, action):
    if current_user != None and \
      current_user.role.has_permission(
        view.model.__snakename__ + '.' + action
      ):
      return True
    assert current_account != None, \
    "You need a organization account for access"
    return current_account.role.has_permission(
      view.model.__snakename__ + '.' + action
    )

class OrganizationSchema(GQLModelSchema, AccountAccessMixin):
  model = Organization
  object_type = OrganizationType


class BusinessAddressSchema(GQLModelSchema, AccountAccessMixin):
  model = BusinessAddress
  object_type = BusinessAddressType
  verbose_name_plural = "BusinessAddresses"
  
  create_fields = [
    "!*",
    "-id",
    "-address.coordinates"
  ]
  update_fields = [
    "!*",
    "-organization",
    '-address.coordinates'
  ]

class AccountRoleSchema(GQLModelSchema, AccountAccessMixin):
  model = AccountRole
  object_type = AccountRoleType
  
class AccountSchema(GQLModelSchema, AccountAccessMixin):
  model = Account
  object_type = AccountType

  my_account = Field(AccountType)

  def resolve_my_account(root, ctx):
    return current_account
  

class AccountGroupSchema(GQLModelSchema, AccountAccessMixin):
  model = AccountGroup
  object_type = AccountGroupType
  


