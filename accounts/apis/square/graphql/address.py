from graphene import (
  String,
  ObjectType,
  InputObjectType
)

class SquareAddressBase:
  address_line_1 = String()
  address_line_2 = String()
  address_line_3 = String()
  locality = String()
  sublocality = String()
  sublocality2 = String()
  sublocality3 = String()
  administrative_district_level_1 = String()
  administrative_district_level_2 = String()
  administrative_district_level_3 = String()
  postal_code = String()
  country = String()
  first_name = String()
  last_name = String()

class SquareAddressType(
  ObjectType, 
  SquareAddressBase
  ):
  pass

class SquareAddressInput(
  InputObjectType, 
  SquareAddressBase
  ):
  pass