from graphene import (
  String,
  Boolean,
  Interface,
  ObjectType
)

class Card(Interface):
  name = String()
  email = String()
  phone_number = String()
  card_type = String()
  brand = String()
  last_4 = String()
  exp_month = String()
  exp_year = String()
  fingerprint = String()
  customer_id = String()
  merchant_id = String()
  reference_id = String()
  enabled = Boolean()

  @classmethod
  def resolve_type(cls, instance, info):
      if instance['prcoessor'] == 'Square':
          return SquareCardType

class SquareCardType(ObjectType):
  class Meta:
    interfaces = (Card, )