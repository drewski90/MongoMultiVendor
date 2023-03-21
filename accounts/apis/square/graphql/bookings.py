from ..client.merchant import square_merchant
from graphene import (
  ID,
  String,
  ObjectType,
  InputObjectType,
  List,
  Boolean,
  Int,
  Mutation,
  Field,
  Argument
)
from .enums import ENUMS

class SquareAvailableBookingType(ObjectType):

  class SquareAvailableAppointmentSegmentType(ObjectType):

    duration_minutes = Int()
    team_member_id = ID()
    service_variation_id = ID()
    service_variation_version = String()

  location_id = ID()
  start_at = String()
  appointment_segments = List(SquareAvailableAppointmentSegmentType)

class SquareBookingType(ObjectType):

  class SquareAppointmentSegmentType(ObjectType):

    duration_minutes = Int()
    service_vartiation_id = ID()
    team_member_id = ID()
    service_variation_version = Int()
    intermission_minutes = Int()
    any_team_member = Boolean()
    resource_ids = List(ID)

  class SquareCreatorDetailsType(ObjectType):
    creator_type = String()
    team_member_id = ID()
    customer_id = ID()
  
  id = ID()
  version = String()
  created_at = String()
  updated_at = String()
  start_at = String()
  location_id = ID()
  customer_id = ID()
  customer_note = String()
  seller_note = String()
  transition_time_minutes = Int()
  all_day = Boolean()
  appointment_segments = List(SquareAppointmentSegmentType)
  creator_details = Field(SquareCreatorDetailsType)
  location_type = String()
  source = String()
  status = String()

class SquareBookingInput(InputObjectType):

  class SquareAppointmentSegmentInput(InputObjectType):

    duration_minutes = Int()
    service_vartiation_id = ID()
    team_member_id = ID()
    service_variation_version = Int()
    intermission_minutes = Int()
    any_team_member = Boolean()
    resource_ids = List(ID)

  class SquareCreatorDetailsInput(InputObjectType):
    creator_type = Argument(ENUMS.SquareBookingCreatorTypeEnum)
    team_member_id = ID()
    customer_id = ID()
  
  id = ID()
  version = String()
  created_at = String()
  updated_at = String()
  start_at = String()
  location_id = ID()
  customer_id = ID()
  customer_note = String()
  seller_note = String()
  transition_time_minutes = Int()
  all_day = Boolean()
  appointment_segments = List(SquareAppointmentSegmentInput)
  creator_details = Field(SquareCreatorDetailsInput)
  location_type = Argument(ENUMS.SquareBookingBookingLocationTypeEnum)
  source = Argument(ENUMS.SquareBookingSourceTypeEnum)
  status = Argument(ENUMS.SquareBokingStatusEnum)

class SquareAppointmentSearchFilterInput(InputObjectType):

  end_at = String()
  start_at = String(required=True)
  location_id = ID(required=True)
  service_variation_ids = List(ID, required=True)
  team_member_ids = List(ID)
  booking_id = String()

class SquareBookingsFilterInput(InputObjectType):
  team_member_id=ID()
  location_id=ID()
  start_at_min=ID()
  start_at_max=ID()

class SquareBookingsPaginationInput(InputObjectType):
  cursor = String()
  limit = Int()

class SquareBookingResultsType(ObjectType):
  bookings = List(SquareBookingType)
  cursor = String()

  def resolve_results(root, ctx):
    return root['bookings']

class SquareCreateBooking(Mutation):

  booking = Field(SquareBookingType)

  class Arguments:
    idempotency_key = String(required=True)
    booking = SquareBookingInput(
      required=True
    )

  @classmethod
  def mutate(cls, root, ctx, idempotency_key, booking):
    booking = square_merchant.bookings.create(
      idempotency_key=idempotency_key,
      **booking
    )
    return cls(booking=booking)

class SquareUpdateBooking(Mutation):

  booking = Field(SquareBookingType)

  class Arguments:

    idempotency_key = String(required=True)
    booking = SquareBookingInput(
      required=True
    )

  @classmethod
  def mutate(cls, root, ctx, idempotency_key, booking):
    booking = square_merchant.bookings.update(
      idempotency_key=idempotency_key,
      **booking
    )
    return cls(booking=booking)

class SquareCancelBooking(Mutation):

  booking = Field(SquareBookingType)

  class Arguments:

    booking_id = ID(required=True)
    idempotency_key = String(required=True)
    booking_version = Int(required=True)
  
  @classmethod
  def mutate(cls, root, ctx, **kwargs):
    result = square_merchant.bookings.cancel(
      **kwargs
    )
    return cls(**result)