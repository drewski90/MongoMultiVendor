from typing import List
from .address import Address
from .error import request_wrapper
from pydantic import constr, confloat
from datetime import datetime
from .utils import APIWrapper, APIModel, Model
from .enums import (
  SquareLocationTypeEnum,
  SquareLocationCapabilitiesEnum,
  SquareTaxIdEnum,
  SquareStatusEnum,
  SquareDayOfWeekEnum,
  SquareTimeZoneEnum
)
from .patterns import (
  LOCAL_TIME_PATTERN,
  RFC_3339_PATTERN,
  EMAIL_PATTERN,
)

class BusinessHoursPeriod(Model):
  day_of_week:SquareDayOfWeekEnum
  start_local_time:constr(regex=LOCAL_TIME_PATTERN)
  end_local_time:constr(regex=LOCAL_TIME_PATTERN)

class BusinessHours(Model):
  periods:List[BusinessHoursPeriod]=[]

class Coordinates(Model):
  longitude:confloat()
  latitude:confloat()

class Location(APIModel):
  
  id:constr(
    strip_whitespace=True, 
    strict=True, 
    max_length=32
    )=None
  name:constr(
    strip_whitespace=True, 
    strict=True, 
    max_length=255
    )=None
  address:Address=None
  timezone:SquareTimeZoneEnum=None
  capabilities:List[SquareLocationCapabilitiesEnum]=None
  status:SquareStatusEnum=None
  merchant_id:constr(
    strip_whitespace=True, 
    strict=True, 
    max_length=32
    )=None
  country:constr(
    strip_whitespace=True, 
    strict=True, 
    max_length=2, 
    min_length=2, 
    to_upper=True
    )=None
  language_code:constr(
    strip_whitespace=True, 
    strict=True,
    max_length=5,
    min_length=2,
    )=None
  currency:constr(
    strip_whitespace=True, 
    strict=True,
    max_length=3,
    min_length=3,
    to_upper=True
    )=None
  phone_number:constr(
    strip_whitespace=True,
    max_length=17,
    )=None
  business_name:constr(
    strip_whitespace=True,
    max_length=255,
    strict=True
    )=None
  type:SquareLocationTypeEnum=None
  website_url:constr(
    strip_whitespace=True,
    max_length=255,
    strict=True
    )=None
  business_email:constr(
    to_lower=True,
    regex=EMAIL_PATTERN, 
    strip_whitespace=True,
  )=None
  description:constr(
    strip_whitespace=True,
    max_length=1024,
    strict=True
    )=None
  twitter_username:constr(
    strip_whitespace=True,
    max_length=15,
    strict=True
    )=None
  instagram_username:constr(
    strip_whitespace=True,
    max_length=30,
    strict=True
    )=None
  facebook_url:constr(
    strip_whitespace=True,
    max_length=255,
    strict=True
    )=None
  logo_url:constr(
    strip_whitespace=True,
    max_length=255,
    strict=True
    )=None
  pos_background_url:constr(
    strip_whitespace=True,
    max_length=255,
    strict=True
    )=None
  mcc:constr(
    strip_whitespace=True,
    min_length=4,
    max_length=4,
    strict=True
    )=None
  full_format_logo_url:constr(
    strip_whitespace=True,
    max_length=255,
    strict=True
    )=None
  tax_ids:List[SquareTaxIdEnum]=None
  business_hours:BusinessHours=None
  coordinates:Coordinates=None
  updated_at:datetime=None
  created_at:datetime=None
  # created_at:constr(
  #   strip_whitespace=True, 
  #   regex=RFC_3339_PATTERN
  #   )=None
  # updated_at:constr(
  #   strip_whitespace=True, 
  #   regex=RFC_3339_PATTERN
  #   )=None

  _edit_fields_ = dict(
    name=True,
    address=True,
    timezone=True,
    status=True,
    country=True,
    language_code=True,
    currency=True,
    phone_number=True,
    business_name=True,
    type=True,
    website_url=True,
    business_email=True,
    description=True,
    twitter_username=True,
    instagram_username=True,
    facebook_url=True,
    logo_url=True,
    pos_background_url=True,
    mcc=True,
    full_format_logo_url=True,
    tax_ids=True,
    business_hours=True,
    coordinates=True,
  )

  def update(self):
    body = request_wrapper(
      self.api.update_location,
      location_id=self.id,
      body={"location":self.update_fields}
    )
    self.refresh(**body['location'])
    return self

  def save(self):
    if self.id:
      return self.update()
    body = request_wrapper(
      self.api.create_location,
      body=dict(location=self.update_fields)
    )
    self.refresh(**body['location'])
    return self

class Locations(APIWrapper):

  api_name = "locations"

  def list(self) -> List[Location]:
    body = request_wrapper(
      self.api.list_locations
    )
    if 'locations' not in body:
      return []
    return [
      Location(
        api_wrapper=self, 
        **location
      ) for location in body['locations']
    ]

  def create(
    self,
    name:str=None,
    address:Address=None,
    timezone:str=None,
    status:str=None,
    country:str=None,
    language_code:str=None,
    currency:str=None,
    phone_number:str=None,
    business_name:str=None,
    type:str=None,
    website_url:str=None,
    business_email:str=None,
    description:str=None,
    twitter_username:str=None,
    instagram_username:str=None,
    facebook_url:str=None,
    logo_url:str=None,
    mcc:str=None,
    full_format_logo_url:str=None,
    tax_ids:List[str]=None,
    business_hours:BusinessHours=None,
    coordinates:Coordinates=None,
  ) -> Location:
    location = Location(
      api_wrapper=self,
      name=name,
      address=address,
      timezone=timezone,
      status=status,
      country=country,
      language_code=language_code,
      currency=currency,
      phone_number=phone_number,
      business_name=business_name,
      type=type,
      website_url=website_url,
      business_email=business_email,
      description=description,
      twitter_username=twitter_username,
      instagram_username=instagram_username,
      facebook_url=facebook_url,
      logo_url=logo_url,
      mcc=mcc,
      full_format_logo_url=full_format_logo_url,
      tax_ids=tax_ids,
      business_hours=business_hours,
      coordinates=coordinates
    )
    location.save()
    return location

  def retrieve(self, location_id:str) -> Location:
    body = request_wrapper(
      self.api.retrieve_location,
      location_id=location_id
    )
    return Location(
      api_wrapper=self,
      **body['location']
    )

  def update(
    self, 
    id:str,
    name:str=None,
    address:Address=None,
    timezone:str=None,
    status:str=None,
    country:str=None,
    language_code:str=None,
    currency:str=None,
    phone_number:str=None,
    business_name:str=None,
    type:str=None,
    website_url:str=None,
    business_email:str=None,
    description:str=None,
    twitter_username:str=None,
    instagram_username:str=None,
    facebook_url:str=None,
    logo_url:str=None,
    mcc:str=None,
    full_format_logo_url:str=None,
    tax_ids:List[str]=None,
    business_hours:BusinessHours=None,
    coordinates:Coordinates=None,
    ) -> Location:
    location = Location(
      api_wrapper=self,
      id=id,
      name=name,
      address=address,
      timezone=timezone,
      status=status,
      country=country,
      language_code=language_code,
      currency=currency,
      phone_number=phone_number,
      business_name=business_name,
      type=type,
      website_url=website_url,
      business_email=business_email,
      description=description,
      twitter_username=twitter_username,
      instagram_username=instagram_username,
      facebook_url=facebook_url,
      logo_url=logo_url,
      mcc=mcc,
      full_format_logo_url=full_format_logo_url,
      tax_ids=tax_ids,
      business_hours=business_hours,
      coordinates=coordinates
    )
    location.update()
    return location


