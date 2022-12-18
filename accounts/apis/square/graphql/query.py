from ..models import SquareOAuth
from graphene import ObjectType, Field, String
from ....sessions import current_org
from .types.square import SquareType

class SquareQueries(ObjectType):
  square = Field(SquareType)
  authorize_square = String()
  
  def resolve_square(r, c):
    return SquareOAuth.objects.get(
      organization=current_org.id
    )