from .error import request_wrapper
from .address import Address
from .cards import Card
from uuid import uuid4
from .utils import APIModel, APIWrapper
from pydantic import constr
from typing import List
from .queries import *
from .patterns import (
  EMAIL_PATTERN, 
  RFC_3339_PATTERN,
  DATE_PATTERN
)
from .enums import (
  SquareTaxIdEnum
)

class Customer(APIModel):

  id:constr(
    strip_whitespace=True, 
    strict=True, 
    max_length=32
    )=None
  given_name:constr(
    strip_whitespace=True,
    strict=True
    )=None
  family_name:constr(
    strip_whitespace=True,
    strict=True
    )=None
  email_address:constr(
    to_lower=True,
    regex=EMAIL_PATTERN,
    strip_whitespace=True,
    strict=True
    )=None
  company_name:constr(
    strip_whitespace=True
    )=None
  nickname:constr(
    strip_whitespace=True,
    max_length=255,
    )=None
  phone_number:constr(
    strip_whitespace=True,
    max_length=17,
    )=None
  reference_id:constr(
    strip_whitespace=True,
    max_length=255,
    strict=True
    )=None
  address:Address=None
  note:constr(
    strip_whitespace=True,
    max_length=1024,
    strict=True
    )=None
  birthday:constr(
    strip_whitespace=True,
    max_length=255,
    regex=DATE_PATTERN,
    strict=True
    )=None
  tax_ids:List[SquareTaxIdEnum]=None
  created_at:constr(
    strip_whitespace=True, 
    regex=RFC_3339_PATTERN
    )=None
  updated_at:constr(
    strip_whitespace=True, 
    regex=RFC_3339_PATTERN
    )=None
  preferences:dict=None
  segment_ids:List[constr(
    strip_whitespace=True
    )]=None
  group_ids:List[constr(
    strip_whitespace=True
    )]=None
  version:int=None
  creation_source:constr(
    strip_whitespace=True,
    max_length=255,
    strict=True
    )=None

  _edit_fields_ = {
    'given_name':True,
    'family_name':True,
    'email_address':True,
    'company_name':True,
    'nickname':True,
    'phone_number':True,
    'reference_id':True,
    'address':True,
    'note':True,
    'birthday':True,
    'tax_ids':True
  }

  @property
  def cards(self):
    return self.merchant.cards.list(
      customer_id=self.id
    ).get('cards', [])

  def add_card(
    self, 
    card_nonce:str,
    billing_address:Address=None,
    cardholder_name:str=None,
    verification_token:str=None
    ):
    body = request_wrapper(
      self.api.create_customer_card,
      customer_id=self.id,
      body=dict(
        card_nonce=card_nonce,
        billing_address=billing_address,
        cardholder_name=cardholder_name,
        verification_token=verification_token
      )
    )
    return Card(
      api_wrapper=self.api_wrapper,
      **body['card']
    )

  def delete_card(self, card_id):
    body = request_wrapper(
      self.api.delete_customer_card,
      customer_id=self.id,
      card_id=card_id
    )
    return body

  def update(self, upsert=False):
    if self.id is None and not upsert:
      raise Exception('cannot update customer without customer id')
    if self.id is None and upsert:
      self.save(idempotency_key=str(uuid4()))
    body = request_wrapper(
      self.api.update_customer,
      customer_id=self.id,
      body=self.update_fields
    )
    self.refresh(**body['customer'])
    return self

  def save(self, idempotency_key=None):
    if self.id:
      return self.update()
    body = request_wrapper(
      self.api.create_customer,
      body=dict(
        idempotency_key=idempotency_key,
        **self.update_fields
      )
    )
    self.refresh(**body['customer'])

  def delete(self):
    return self.merchant.customers.delete(
      self.id
    )

class Customers(APIWrapper):

  api_name = "customers"

  def create(
    self, 
    idempotency_key:str=None,
    given_name:str=None,
    family_name:str=None,
    email_address:str=None,
    company_name:str=None,
    nickname:str=None,
    phone_number:str=None,
    reference_id:str=None,
    address:dict=None,
    note:str=None,
    birthday:str=None,
    tax_ids:str=None
    ) -> Customer:
    customer = Customer(
      api_wrapper=self,
      given_name=given_name,
      family_name=family_name,
      email_address=email_address,
      company_name=company_name,
      nickname=nickname,
      phone_number=phone_number,
      reference_id=reference_id,
      address=address,
      note=note,
      birthday=birthday,
      tax_ids=tax_ids
    )
    customer.save(
      idempotency_key=idempotency_key
    )
    return customer

  def retrieve(self, customer_id):
    body = request_wrapper(
      self.api.retrieve_customer,
      customer_id=customer_id
    )
    assert 'customer' in body, "Customer does not exist"
    return Customer(
      api_wrapper=self,
      **body['customer']
    )
  
  def update(
      self, 
      id:str,
      given_name:str=None,
      family_name:str=None,
      email_address:str=None,
      company_name:str=None,
      nickname:str=None,
      phone_number:str=None,
      reference_id:str=None,
      address:dict=None,
      note:str=None,
      birthday:str=None,
      tax_ids:str=None
    ):
    customer = Customer(
      api_wrapper=self,
      id=id,
      given_name=given_name,
      family_name=family_name,
      email_address=email_address,
      company_name=company_name,
      nickname=nickname,
      phone_number=phone_number,
      reference_id=reference_id,
      address=address,
      note=note,
      birthday=birthday,
      tax_ids=tax_ids
    )
    customer.update()
    return customer

  def list(
    self,
    cursor=None, 
    limit=None,
    sort_field:str=None,
    sort_order:str=None,
    creation_source_any:List[str]=None,
    creation_source_none:List[str]=None,
    created_at_start:str=None,
    created_at_end:str=None,
    updated_at_start:str=None,
    updated_at_end:str=None,
    email_address_fuzzy:str=None,
    email_address:str=None,
    phone_number_fuzzy:str=None,
    phone_number:str=None,
    reference_id_fuzzy:str=None,
    reference_id:str=None,
    group_ids_any:List[str]=None,
    group_ids_all:List[str]=None,
    group_ids_none:List[str]=None,
    custom_attributes:List[dict]=None,
    segment_ids_any:List[str]=None,
    segment_ids_all:List[str]=None,
    segment_ids_none:List[str]=None,
    ) -> dict:
    request = {}
    filter = {}
    if email_address or email_address_fuzzy:
      filter['email_address'] = add_text_filter(
        exact=email_address,
        fuzzy=email_address_fuzzy
      )
    if phone_number or phone_number_fuzzy:
      filter['phone_number'] = add_text_filter(
        exact=phone_number,
        fuzzy=phone_number_fuzzy
      )
    if reference_id or reference_id_fuzzy:
      filter['reference_id'] = add_text_filter(
        exact=reference_id,
        fuzzy=reference_id_fuzzy
      )
    if creation_source_any or creation_source_none:
      assert not (creation_source_any and creation_source_none), \
        'creation_source_in and creation_source_not_in cannot be used together'
      if creation_source_any:
        filter['creation_source'] = add_value_rule_filter(
          values=creation_source_none,
          include_values=True
        )
      if creation_source_none:
        filter['creation_source'] = add_value_rule_filter(
          values=creation_source_none,
          include_values=False
        )
    if created_at_start or created_at_end:
      filter['created_at'] = add_date_range_filter(
        start=created_at_start,
        end=created_at_end
      )
    if updated_at_start or updated_at_end:
      filter['updated_at'] = add_date_range_filter(
        start=updated_at_start,
        end=updated_at_end
      )
    if group_ids_all or group_ids_any or group_ids_none:
      filter['group_ids'] = add_value_filter(
        all=group_ids_all,
        none=group_ids_none,
        any=group_ids_any
      )
    if segment_ids_any or segment_ids_all or segment_ids_none:
      filter['segment_ids'] = add_value_filter(
        all=segment_ids_all,
        any=segment_ids_any,
        none=segment_ids_none
      )
    if custom_attributes:
      filter['custom_attribute'] = {
        "filters": custom_attributes
      }
    query = {}
    request['query'] = query
    if sort_field and sort_order:
      query['sort'] = {
        'field': sort_field,
        'sort_order': sort_order
      }
    if len(filter) > 0:
      query['filter'] = filter
    if cursor:
      request['cursor'] = cursor
    if limit:
      request['limit'] = limit
    body = request_wrapper(
      self.api.search_customers,
      body=request
    )
    if len(body) == 0:
      return {"customers": []}
    body['customers'] = [
      Customer(
        api_wrapper=self,
        **customer
      ) for customer in body['customers']
    ]
    return body

  def delete(self, customer_id):
    return request_wrapper(
      self.api.delete_customer,
      customer_id=customer_id
    )

  def create_card(
    self, 
    customer_id:str,
    card_nonce:str,
    billing_address:Address=None,
    cardholder_name:str=None,
    verification_token:str=None
    ) -> Card:
    body = request_wrapper(
      self.api.create_customer_card,
      customer_id=customer_id,
      body=dict(
        card_nonce=card_nonce,
        billing_address=billing_address,
        cardholder_name=cardholder_name,
        verification_token=verification_token
      )
    )
    return Card(
      api_wrapper=self,
      **body['card']
    )

  def delete_card(
    self,
    customer_id:str,
    card_id:str
  ) -> dict:
    body = self.api.delete_customer_card(
      customer_id=customer_id,
      card_id=card_id
    )
    return body

  def add_group_to_customer(
    self,
    customer_id:str, 
    group_id:str):
    return self.api.add_group_to_customer(
      customer_id, 
      group_id
    )

  def remove_group_from_customer(
    self,
    customer_id:str, 
    group_id:str):
    return self.api.remove_group_from_customer(
      customer_id, 
      group_id
    )

import json
with open('data.json', 'w') as f:
    json.dump(Customer.schema(), f)