from ...graphql import MongoType, ObjectId, Media, Date
from ...users.graphql import (
  UserType, 
  UserRoleType, 
)
from ...users.graphql.types import AddressType
from graphene import (
  ObjectType,
  String,
  Boolean,
  Field,
  Int,
  List,
  DateTime
)

class OrganizationType(MongoType):
  logo = Media()
  name = String()
  required_account_approval = Boolean()
  status = String()
  created = DateTime()
  updated = DateTime()
  payment_processors = List(String)

class BusinessDayType(ObjectType):
  start_hour = Int()
  start_minutes = Int()
  end_hour = Int()
  end_minutes = Int()

class BusinessHoursType(ObjectType):
  timezone = String()
  sunday = Field(BusinessDayType)
  monday = Field(BusinessDayType)
  tuesday = Field(BusinessDayType)
  wednesday = Field(BusinessDayType)
  thursday = Field(BusinessDayType)
  friday = Field(BusinessDayType)
  saturday = Field(BusinessDayType)

class OrganizationLocationType(MongoType):
  address = Field(AddressType)
  organization = Field(OrganizationType)
  location_name = String()
  business_hours = Field(BusinessHoursType)
  created = DateTime()
  updated = DateTime()

class AccountRoleType(UserRoleType):
  organization = ObjectId()
  is_admin = Boolean()

class AccountGroupType(MongoType):
  organization = ObjectId()
  name = String()

class AccountType(MongoType):
  user = Field(UserType)
  role = Field(AccountRoleType)
  organization = Field(OrganizationType)
  groups = List(AccountGroupType)
  status = String()
  created = DateTime()

