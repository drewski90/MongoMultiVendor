from .card import Card
from graphene import (
  Interface,
  String,
  Field,
  ObjectType
)
class PaymentMethod(Interface):
  id = String()
  card = Field(Card)
  type = String()

  @classmethod
  def resolve_type(cls, instance, info):
      if instance.type == 'SQUARE':
          return SquarePaymentMethodType

class SquarePaymentMethodType(ObjectType):
  class Meta:
    interfaces = (PaymentMethod, )