from .error import request_wrapper
from .utils import APIModel, APIWrapper
from pydantic import constr, conint
from typing import Any
from .address import Address
from .enums import (
  SquareCardBrandEnum,
  SquareCardPrepaidTypeEnum,
  SquareCardTypeEnum,
  SquareCardCoBrandEnum
)

class Card(APIModel):
  id:constr(
    strip_whitespace=True, 
    strict=True, 
    max_length=64
    )=None
  card_brand:SquareCardBrandEnum=None
  card_type:SquareCardTypeEnum=None
  last_4:constr(max_length=4)=None
  exp_month:conint(lt=12)=None
  exp_year:conint(lt=10000, gt=1970)=None
  cardholder_name:constr(
    strip_whitespace=True, 
    strict=True, 
    max_length=96
    )=None
  billing_address:Address
  fingerprint:constr(
    strip_whitespace=True, 
    strict=True, 
    max_length=255
    )
  customer_id:constr(
    strip_whitespace=True, 
    strict=True, 
    max_length=255
    )
  merchant_id:constr(
    strip_whitespace=True, 
    strict=True, 
    max_length=255
    )
  reference_id:constr(
    strip_whitespace=True, 
    strict=True, 
    max_length=128
    )=None
  enabled:bool
  card_type:SquareCardTypeEnum
  prepaid_type:SquareCardPrepaidTypeEnum
  bin:constr(
    strip_whitespace=True, 
    strict=True, 
    max_length=6
    )
  version:int
  card_co_brand:SquareCardCoBrandEnum=None

  def disable(self):
    if self.id is not None:
      return self.api.disable(self.id)

class Cards(APIWrapper):

  api_name = "cards"

  def create(
    self, 
    idempotency_key:str, 
    source_id:str,
    card:dict,
    verification_token:str=None,
    ):
    body = request_wrapper(
      self.api.create_card,
      body=dict(
        idempotency_key=idempotency_key,
        source_id=source_id,
        card=card,
        verification_token=verification_token
      )
    )
    return Card(
      api_wrapper=self,
      **body['card']
    )
  
  def list(
      self,
      cursor:str=None,
      customer_id:str=None,
      reference_id:str=None,
      sort_order:str=None,
      include_disabled:bool=True
    ) -> dict:
    body = request_wrapper(
      self.api.list_cards,
      cursor=cursor,
      customer_id=customer_id,
      include_disabled=str(include_disabled),
      reference_id=reference_id,
      sort_order=sort_order
    )
    if 'cards' in body:
      body['cards'] = [
        Card(
          api_wrapper=self,
          **card
        ) for card in body['cards']
      ]
    else:
      body['cards'] = []
    return body

  def retrieve(self, card_id):
    body = request_wrapper(
      self.api.retrieve_card,
      card_id=card_id
    )
    return Card(
      api_wrapper=self,
      **body['card']
    )

  def disable(self, card_id):
    body = request_wrapper(
      self.api.disable_card,
      card_id=card_id
    )
    return Card(
      api_wrapper=self,
      **body['card']
    )

