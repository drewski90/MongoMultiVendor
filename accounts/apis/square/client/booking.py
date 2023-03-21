from .utils import APIModel, APIWrapper, Model
from pydantic import constr, conint
from .patterns import RFC_3339_PATTERN
from .error import request_wrapper
from uuid import uuid4
from typing import List
from .enums import (
  SquareBookingStatusEnum,
  SquareBookingBookingSourceEnum,
  SquareBookingCreatorDetailsCreatorTypeEnum,
  SquareBusinessAppointmentSettingsBookingLocationTypeEnum
)

class Booking(APIModel):

  class AppointmentSegment(Model):
    service_variation_id:constr(
      max_length=26, 
      strip_whitespace=True,
      strict=True
    )
    team_member_id:constr(
      max_length=32,
      strip_whitespace=True,
      strict=True
    )
    duration_minutes:conint(lt=1500)=None
    service_variation_version:conint()=None
    intermission_minutes:conint()=None
    any_team_member:bool=None
    resource_ids:List[constr(
      strip_whitespace=True, 
      min_length=1
      )]

  class BookingCreatorDetails(Model):
    creator_type:str
    team_member_id:constr(
      max_length=32,
      strip_whitespace=True,
    )=None
    customer_id:constr(
      max_length=192,
      strip_whitespace=True
    )=None

  id:constr(
    max_length=36, 
    strip_whitespace=True,
    strict=True
  )=None
  version:int=None
  status:SquareBookingStatusEnum=None
  created_at:constr(
    strip_whitespace=True, 
    regex=RFC_3339_PATTERN
    )=None
  updated_at:constr(
    strip_whitespace=True, 
    regex=RFC_3339_PATTERN
    )=None
  start_at:constr(
    strip_whitespace=True, 
    regex=RFC_3339_PATTERN
    )=None
  location_id:constr(
    max_length=32, 
    strip_whitespace=True,
    strict=True
  )=None
  customer_id:constr(
    max_length=192, 
    strip_whitespace=True,
    strict=True
  )=None
  customer_note:constr(
    max_length=4096, 
    strip_whitespace=True,
    strict=True
  )=None
  seller_note:constr(
    max_length=4096, 
    strip_whitespace=True,
    strict=True
  )=None
  appointment_segments:List[AppointmentSegment]=None
  transition_time_minutes:int=None
  all_day:bool=None
  location_type:SquareBusinessAppointmentSettingsBookingLocationTypeEnum=None
  creator_details:SquareBookingCreatorDetailsCreatorTypeEnum=None
  source:SquareBookingBookingSourceEnum=None

  def save(self, idempotency_key=None):
    if self.id:
      return self.update(idempotency_key)
    body = request_wrapper(
      self.api.create_booking,
      body=dict(
        idempotency_key=idempotency_key,
        booking=self.dict(
          exclude_none=True, 
          exclude_unset=True
        )
      )
    )
    self.refresh(**body['booking'])
    return self

  def update(self, idempotency_key=None):
    body = request_wrapper(
      self.api.update_booking,
      booking_id=self.id,
      body=dict(
        idempotency_key=idempotency_key,
        booking=self.dict(
          exclude_none=True, 
          exclude_unset=True
        )
      )
    )
    self.refresh(**body['booking'])
    return self

  def cancel(
    self, 
    idempotency_key:str=None, 
    booking_version:int=None
  ):
    body = request_wrapper(
      self.api.cancel_booking,
      booking_id=self.id,
      body=dict(
        idempotency_key=idempotency_key,
        booking_version=booking_version
      )
    )
    return body

class Availability(Model):
  start_at:str
  location_id:str=None
  appoinment_segments:List[Booking.AppointmentSegment]=None

class Bookings(APIWrapper):

  api_name = "bookings"

  def search_availability(
    self,
    start_at:str,
    location_id:str,
    segment_filters:List[str],
    end_at:str=None,
    booking_id:str=None
    ) -> List[Availability]:
    body = request_wrapper(
      self.api.search_availability,
      body=dict(
        query=dict(
          filter=dict(
            start_at_range=dict(
              start_at=start_at,
              end_at=end_at
            ),
            location_id=location_id,
            segment_filters=segment_filters,
            booking_id=booking_id
          )
        )
      )
    )
    return body['availabilities']

  def list(
    self,
    limit=None,
    cursor=None,
    team_member_id=None,
    location_id=None,
    start_at_min=None,
    start_at_max=None
    ) -> dict:
    body = request_wrapper(
      self.api.list_bookings,
      limit=limit,
      cursor=cursor,
      team_member_id=team_member_id,
      location_id=location_id,
      start_at_min=start_at_min,
      start_at_max=start_at_max
    )
    if 'bookings' in body:
      body['bookings'] = [
        Booking(
          api_wrapper=self, 
          **booking
        ) for booking in body['bookings']
      ]
    else:
      body['bookings'] = []
    return body

  def create(
    self,
    id:str,
    version:int,
    created_at:str,
    updated_at:str,
    idempotency_key:str,
    status:SquareBookingStatusEnum=None,
    start_at:str=None,
    location_id:str=None,
    customer_id:str=None,
    customer_note:str=None,
    seller_note:str=None,
    appointment_segments:List[Booking.AppointmentSegment]=None,
    transition_time_minutes:int=None,
    all_day:bool=None,
    location_type:SquareBusinessAppointmentSettingsBookingLocationTypeEnum=None,
    creator_details:SquareBookingCreatorDetailsCreatorTypeEnum=None,
    source:SquareBookingBookingSourceEnum=None
  ) -> Booking:
    booking = Booking(
      api_wrapper=self,
      id=id,
      created_at=created_at,
      updated_at=updated_at,
      version=version,
      status=status,
      start_at=start_at,
      location_id=location_id,
      customer_id=customer_id,
      customer_note=customer_note,
      seller_note=seller_note,
      appointment_segments=appointment_segments,
      transition_time_minutes=transition_time_minutes,
      all_day=all_day,
      location_type=location_type,
      creator_details=creator_details,
      source=source
    )
    booking.save(idempotency_key)
    return booking
  
  def update(
    self, 
    id:str,
    version:int,
    created_at:str,
    updated_at:str,
    idempotency_key:str,
    status:SquareBookingStatusEnum=None,
    start_at:str=None,
    location_id:str=None,
    customer_id:str=None,
    customer_note:str=None,
    seller_note:str=None,
    appointment_segments:List[Booking.AppointmentSegment]=None,
    transition_time_minutes:int=None,
    all_day:bool=None,
    location_type:SquareBusinessAppointmentSettingsBookingLocationTypeEnum=None,
    creator_details:SquareBookingCreatorDetailsCreatorTypeEnum=None,
    source:SquareBookingBookingSourceEnum=None
  ):
    booking = Booking(
      api_wrapper=self,
      id=id,
      created_at=created_at,
      updated_at=updated_at,
      version=version,
      status=status,
      start_at=start_at,
      location_id=location_id,
      customer_id=customer_id,
      customer_note=customer_note,
      seller_note=seller_note,
      appointment_segments=appointment_segments,
      transition_time_minutes=transition_time_minutes,
      all_day=all_day,
      location_type=location_type,
      creator_details=creator_details,
      source=source
    )
    booking.update(idempotency_key)
    return booking

  def cancel(
    self, 
    booking_id, 
    idempotency_key:str=None,
    booking_version:int=None
    ):
    booking = Booking(
      api_wrapper=self,
      id=booking_id
      )
    booking.cancel(
      idempotency_key=idempotency_key,
      booking_version=booking_version
    )
    return booking

  def retrieve(
    self, 
    booking_id:str
    ):
    body = request_wrapper(
      self.api.retrieve_booking,
      booking_id=booking_id
    )
    return Booking(
      api_wrapper=self,
      **body['booking']
    )