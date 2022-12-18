from .catalog import SquareCatalogType
from .location import SquareLocationType
from .booking import SquareBookingType
from ...utils import get
from graphene import (
  ObjectType,
  Field,
  List
)

class SquareType(ObjectType):
  catalog = Field(SquareCatalogType)
  locations = List(SquareLocationType)
  bookings = List(SquareBookingType)

  def catalog(r,c):
    return 