from .types import (
  Customer,
  SquareCustomerType,
  PaymentMethod,
  SquarePaymentMethodType,
  LocationType
)
from ..utils import get_processor
from graphene import (
  ObjectType,
  Field,
  Enum,
  String,
  Argument,
  List,
  ID
)
from graphene.types.generic import GenericScalar
from .enum import PaymentProcessors
from ...sessions import current_user


class PaymentsQueries(ObjectType):
  wallet = Field(
    Customer, 
    processor=Argument(PaymentProcessors, required=True)
  )
  locations = List(LocationType)
  bookings = GenericScalar()
  team = GenericScalar()
  availability  = GenericScalar(
    start_date = String(),
    location_id = ID(required=True),
    service_variation_ids = List(ID, required=True),
    team_member_ids = List(ID)
  )
  catalog = GenericScalar(processor=Argument(PaymentProcessors))

  def resolve_catalog(root, ctx, processor):
    return get_processor(processor).catalog.list()

  def resolve_availability(root, ctx, **kwargs):
    return get_processor('square').bookings.avaliability(**kwargs)

  def resolve_bookings(root, ctx):
    return get_processor('square').bookings.list()

  def resolve_locations(root, ctx):
    return get_processor('square').locations.list()

  def resolve_team(root, ctx):
    return get_processor('square').team.list()

  def resolve_wallet(root, ctx, processor=None):
    pp = get_processor(processor)
    result = pp.customers.retrieve(current_user)
    return result
