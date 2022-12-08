from ...graphql import (
  MongoType, 
  Media,
  AddressType
)
from graphene import (
  String,
  Boolean, 
  DateTime,
  List,
  Field,
  Interface,
  ObjectType
)

class PermissionType(MongoType):
  model = String()
  action = String()
  description = String()

class UserGroupType(MongoType):
  name = String()
  active = Boolean()
  created = DateTime()

class UserRoleType(MongoType):
  name = String()
  permissions = List(String)
  created = DateTime()
  is_admin = Boolean()
  default = Boolean()

  def resolve_permissions(root, ctx):
    return [i.action for i in root.permissions]

class UserType(MongoType):
  avatar = Media()
  email = String()
  phone_number = String()
  email_verified = Boolean()
  first_name = String()
  last_name = String()
  groups = List(UserGroupType)  
  role = Field(UserRoleType)
  addresses = List(AddressType)
  status = String()
  created = DateTime()
