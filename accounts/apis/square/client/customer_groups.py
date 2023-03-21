from .utils import APIWrapper, APIModel
from pydantic import constr
from .patterns import RFC_3339_PATTERN
from .error import request_wrapper
from uuid import uuid4
from typing import List

class CustomerGroup(APIModel):

  id:constr(strip_whitespace=True, max_length=255)=None
  name:constr(strip_whitespace=True, min_length=1)=None
  created_at:constr(
    strip_whitespace=True, 
    regex=RFC_3339_PATTERN
    )=None
  updated_at:constr(
    strip_whitespace=True, 
    regex=RFC_3339_PATTERN
    )=None

  _edit_fields_ = {
    "name":True
  }
  
  def save(self, idempotency_key=None):
    if self.id:
      return self.update()
    body = request_wrapper(
      self.api.create_customer_group,
      body = {
        "idempotency_key": idempotency_key,
        "group": self.dict(
          exclude={'id':True},
          exclude_none=True, 
          exclude_unset=None
        )
      }
    )
    self.refresh(**body['group'])
    return self
  
  def delete(self):
    body = request_wrapper(
      self.api.delete_customer_group,
      group_id=self.id
    )
    return body
  
  def update(self):
    body = request_wrapper(
      self.api.update_customer_group,
      group_id=self.id,
      body=dict(
        group=self.dict(
          exclude_none=True, 
          exclude_unset=None
        )
      )
    )
    self.refresh(**body['group'])

  def add_customer(self, customer_id:str):
    body = request_wrapper(
      self.merchant.customers.add_group_to_customer,
      customer_id=customer_id,
      group_id=self.id
    )
    return body

  def remove_customer(self, customer_id:str):
    body = request_wrapper(
      self.merchant.customers.remove_group_from_customer,
      customer_id=customer_id,
      group_id=self.id
    )
    return body

class CustomerGroups(APIWrapper):
  
  api_name = "customer_groups"

  def create(
    self, 
    idempotency_key:str,
    group:CustomerGroup
    ) -> CustomerGroup:
    group = CustomerGroup(
      api_wrapper=self,
      **group
    )
    group.save(idempotency_key)
    return group

  def update(
    self,
    id:str,
    name:str,
    updated_at:str=None,
    created_at:str=None
    ):
    group = CustomerGroup(
      api_wrapper=self,
      id=id,
      name=name,
      updated_at=updated_at,
      created_at=created_at
    )
    group.update()
    return group

  def delete(
    self,
    group_id:str
  ):
    CustomerGroup(
      api_wrapper=self,
      id=group_id
    ).delete()

  def list(
    self, 
    cursor=None, 
    limit=None
    ) -> dict:
    body = request_wrapper(
      self.api.list_customer_groups,
      cursor=cursor,
      limit=limit
    )
    if 'groups' in body:
      body['groups'] = [
        CustomerGroup(
          api_wrapper=self,
          **group
        ) for group in body['groups']
      ]
    else:
      body['groups'] = []
    return body

  def retrieve(
    self, 
    group_id:str
    ) -> CustomerGroup:
    body = request_wrapper(
      self.api.retrieve_customer_group,
      group_id=group_id
    )
    return CustomerGroup(
      api_wrapper=self,
      **body['group']
    )