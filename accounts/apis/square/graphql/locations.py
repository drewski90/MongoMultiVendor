from graphene import (
  String,
  List,
  ObjectType,
  Enum,
  ID,
  Argument,
  Field,
  InputObjectType,
  Mutation
)
from .enums import ENUMS
from .address import SquareAddressType, SquareAddressInput
from ..client.merchant import square_merchant

class Location:

  class SquareLocationCoordinatesType(ObjectType):
    longitude=String()
    latitude=String()

  class SquareBusinessHoursType(ObjectType):

    class SquareBusinessHoursPeriodType(ObjectType):
      day_of_week = String()
      start_local_time = String()
      end_local_time = String()

    periods = List(SquareBusinessHoursPeriodType)

  name=String()
  address=Field(SquareAddressType)
  timezone=String()
  capabilities=List(String)
  status=String()
  merchant_id=String()
  country=String()
  language_code=String()
  currency=String()
  phone_number=String()
  business_name=String()
  type=String()
  website_url=String()
  business_email=String()
  description=String()
  twitter_username=String()
  instagram_username=String()
  facebook_url=String()
  logo_url=String()
  pos_background_url=String()
  mcc=String()
  full_format_logo_url=String()
  tax_ids=List(String)
  business_hours=Field(SquareBusinessHoursType)
  coordinates=Field(SquareLocationCoordinatesType)
  id = ID()
  created_at=String()
  updated_at=String()

class SquareBusinessHoursInput(InputObjectType):

  class SquareBusinessHoursPeriodInput(InputObjectType):
    day_of_week = Argument(ENUMS.SquareDayOfWeekEnum)
    start_local_time = String()
    end_local_time = String()

  periods = List(SquareBusinessHoursPeriodInput)

class SquareLocationCoordinatesInput(InputObjectType):
  longitude=String()
  latitude=String()

class SquareLocationInput(InputObjectType, Location):
  id = ID()
  type =  Argument(ENUMS.SquareLocationTypeEnum)
  business_hours = SquareBusinessHoursInput()
  coordinates = SquareLocationCoordinatesInput()
  address = SquareAddressInput()
  status = Argument(ENUMS.SquareStatusEnum)
  capabilities = List(ENUMS.SquareLocationCapabilitiesEnum)
  tax_ids = List(ENUMS.SquareTaxIdEnum)

class SquareLocationType(ObjectType, Location):
  pass

class SquareUpdateLocation(Mutation):

  location = Field(SquareLocationType)

  class Arguments:
    location = SquareLocationInput(required=True)

  @classmethod
  def mutate(cls, root, ctx, location):
    location = square_merchant.locations.update(
      **location
    )
    return cls(location=location)

class SquareCreateLocation(Mutation):
  
  location = Field(SquareLocationType)

  class Arguments:
    location = SquareLocationInput(required=True)

  @classmethod
  def mutate(cls, root, ctx, location):
    location = square_merchant.locations.create(
      **location
    )
    return cls(location=location)

