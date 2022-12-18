from graphene import (
  String,
  ObjectType, 
  ID,
  Field,
  List
)
from .....graphql import Address

class SquareLocationType(ObjectType):
  id = ID()
  name = String()
  address = Field(Address)
  timezone = String()
  capabilities = List(String)
  status = String()
  created = String()
  merchant_id = String()
  country = String()
  language_code = String()
  currency = String()
  phone_number = String()
  business_name = String()
  type = String()
  website = String()
  business_email = String()
  description = String()
  twitter_username = String()
  instagram_username = String()
  facebook_url = String()
  logo_url = String()
  pos_background_url = String()
  mcc = String()
  full_format_logo_url = String()
  tax_ids = List(String)
  
