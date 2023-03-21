from graphene import (
  String,
  ObjectType,
  Field,
  Boolean,
  Int,
  List,
  InputObjectType,
  ObjectType,
  Mutation,
  ID,
  Argument
)
from .address import (
  SquareAddressType,
  SquareAddressInput
)
from .enums import ENUMS
from ..client.merchant import square_merchant
from .utils import make_timestamp

class Card:
  card_brand = String()
  last_4 = String()
  exp_month = Int()
  exp_year = Int()
  cardholder_name = String()
  billing_address = Field(SquareAddressType)
  fingerprint = String()
  customer_id = String(required=True)
  merchant_id = String()
  reference_id = String()
  enabled = Boolean()
  card_type = String()
  prepaid_type = String()
  bin = String()
  version = Int()
  card_co_brand = String()

class SquareCardType(ObjectType, Card):
  id = String()

class SquareCardResultsType(ObjectType):
  cursor = String()
  results = List(SquareCardType)

  def resolve_results(root, ctx):
    return root['cards']

class SquareCardInput(InputObjectType, Card):
  billing_address = SquareAddressInput()
  card_brand = Argument(ENUMS.SquareCardTypeEnum)
  card_type = Argument(ENUMS.SquareCardTypeEnum)
  prepaid_type = Argument(ENUMS.SquareCardPrepaidTypeEnum)
  card_co_brand = Argument(ENUMS.SquareCardCoBrandEnum)

class SquareDisableCard(Mutation):

  updated_at = String()

  class Arguments:
    card_id = ID()

  def mutate(root, ctx, card_id):
    card = square_merchant.cards.disable(
      card_id
    )
    return SquareDisableCard(
      updated_at=make_timestamp()
    )

class SquareCreateCard(Mutation):
  
  card = Field(SquareCardType)

  class Arguments:
    idempotency_key = String()
    source_id = ID(required=True)
    card = SquareCardInput(required=True)
    verification_token = String()

  def mutate(root, ctx, **kwargs):
    result = square_merchant.cards.create(
      **kwargs
    )
    return SquareCreateCard(
      card = result
    )

class SquareCardFilterInput(InputObjectType):
  customer_id=ID()
  include_disabled=Boolean()
  reference_field = String()

class SquareCardsPaginationInput(InputObjectType):
  cursor = String()
  sort_order = Argument(ENUMS.SquareSortOrderEnum)

class SquareCardResultsType(ObjectType):
  cards = List(SquareCardType)
  cursor = String()