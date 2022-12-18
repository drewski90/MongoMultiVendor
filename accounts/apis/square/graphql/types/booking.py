from graphene.types.generic import GenericScalar
from graphene import (
  ObjectType,
  String,
  Boolean,
  ID,
  Int,
  List
)

class AppointmentSegmentType(ObjectType):
  duration_minutes = Int()
  team_member_id = ID()
  service_variation_id = ID()
  service_variation_version = Int()

class SquareAvailableBookingType(ObjectType):
  location_id = ID()
  start_at = String()
  segments = List(AppointmentSegmentType)
  resolve_segments = lambda r,c:r['appointment_segments']

class SquareCreatorDetailsType(ObjectType):
  creator_type = String()
  team_member_id = ID()
  customer_id = ID()

class SquareBookingType(ObjectType):
  id = ID()
  version = Int()
  status = String()
  created = String()
  resolve_created = lambda r,c:r['created_at']
  updated = String()
  resolve_updated = lambda r,c:r['updated_at']
  start = String()
  resolve_start = lambda r,c:r['start_at']
  location_id = ID()
  customer_id = ID()
  customer_note = String()
  seller_note = String()
  appointment_segments = List(String)
  transition_time_minutes = Int()
  all_day = Boolean()
  location_type = String()
  source = String()
  creator_details = String()

class SquareBookingsType(ObjectType):
  availability = List(
    SquareAvailableBookingType,
    start_date = String(),
    location_id = ID(required=True),
    service_variation_ids = List(ID, required=True),
    team_member_ids = List(ID)
  )
  bookings = List(SquareBookingType)

  def resolve_availability(root, ctx, **kwargs):
    return root.bookings.availability(**kwargs)

  def resolve_bookings(root, ctx):
    return root.bookings.list()