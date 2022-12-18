from graphene.types.generic import GenericScalar
from .catalog import SquareCatalogType
from .location import SquareLocationType
from .booking import SquareBookingsType
from .customer import SquareCustomerType
from .....sessions import current_user
from graphene import (
  ObjectType,
  Field,
  List
)

class SquareType(ObjectType):

  wallet = Field(SquareCustomerType)
  locations = List(SquareLocationType)
  team = GenericScalar()
  bookings = Field(SquareBookingsType)
  catalog = Field(SquareCatalogType)

  def resolve_catalog(root, ctx):
    """returns a unorganized list of jank to sort through"""
    return root.catalog.list()

  def resolve_bookings(root, ctx):
    return root

  def resolve_locations(root, ctx):
    return root.locations.list()

  def resolve_team(root, ctx):
    return root.team.list()

  def resolve_wallet(root, ctx, processor=None):
    result = root.customers.retrieve(current_user)
    return result
