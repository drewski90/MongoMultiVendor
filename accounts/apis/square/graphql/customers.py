from graphene import (
  ObjectType,
  Mutation,
  Field,
  String,
  Boolean,
  List,
  Int,
  InputObjectType,
  ID,
  Argument
)
from graphene.types.generic import GenericScalar
from .address import (
  SquareAddressType, 
  SquareAddressInput
)
from .enums import ENUMS
from .cards import SquareCardType
from ....graphql import Graph
from ..client.merchant import square_merchant
from .utils import make_timestamp
from .filters import *

class CustomerBase:

  given_name = String()
  family_name = String()
  email_address = String()
  company_name = String()
  nickname = String()
  phone_number = String()
  reference_id = String()
  address = Field(SquareAddressType)
  note = String()
  birthday = String()
  tax_ids = List(String)

class SquareCustomerType(ObjectType, CustomerBase):

  id = ID()
  version = Int()
  creation_source = String()
  created_at = String()
  updated_at = String()
  preferences = GenericScalar()
  segment_ids = List(String)
  group_ids = List(String)
  cards = List(SquareCardType)

  def resolve_cards(r, c):
    return r.cards

class SquareCustomerFilterInput(InputObjectType):
  class SquareCustomAttributeFiltersInput(InputObjectType):
    class SquareCustomAttributeFilter(InputObjectType):
      class SquareCustomAttributeFilterValueType(InputObjectType):
        class SquareCustomerAddressFilterInput(InputObjectType):
          postal_code = SquareCustomerTextFilterInput()
          country = String()
        email = Field(SquareCustomerTextFilterInput)
        phone = Field(SquareCustomerTextFilterInput)
        text = Field(SquareCustomerTextFilterInput)
        selection = Field(SquareFilterValueInput)
        date = Field(SquareTimeRangeInputType)
        number = Field(SquareFloatNumberRange)
        boolean = Boolean()
        address = Field(SquareCustomerAddressFilterInput)
      key = String()
      filter = Field(SquareCustomAttributeFilterValueType)
      updated_at = Field(SquareTimeRangeInputType)
    filters = List(SquareCustomAttributeFilter)
  creation_source_any = List(String)
  creation_source_none = List(String)
  created_at_start = String()
  created_at_end = String()
  updated_at_start = String()
  updated_at_end = String()
  email_address = String()
  email_address_fuzzy = String()
  phone_number = String()
  phone_number_fuzzy = String()
  reference_id = String()
  reference_id_fuzzy = String()
  group_ids_any = List(String)
  group_ids_all = List(String)
  group_ids_none = List(String)
  custom_attributes = Field(SquareCustomAttributeFiltersInput)
  segment_ids_any = List(String)
  segment_ids_all = List(String)
  segment_ids_none = List(String)

class SquareCustomersPaginationInput(InputObjectType):
  cursor = String()
  limit = Int()
  sort_field = String()
  sort_order = Argument(ENUMS.SquareSortOrderEnum)

class SquareCustomerResultsType(ObjectType):
  cursor = String()
  customers = List(SquareCustomerType)

class SquareCustomerInput(InputObjectType, CustomerBase):

  id = ID(required=True)
  address = Field(SquareAddressInput)

class SquareUpdateCustomer(Mutation):

  customer = Field(SquareCustomerType)

  class Arguments:

    customer = SquareCustomerInput(
      required=True
    )

  @classmethod
  def mutate(cls, root, ctx, customer):
    customer = square_merchant.customers.update(**customer)
    return cls(customer=customer)

class SquareDeleteCustomer(Mutation):

  updated_at = String()

  class Arguments:
    customer_id = ID(required=True)
  
  @classmethod
  def mutate(cls, root, ctx, customer_id):
    square_merchant.customers.delete(customer_id)
    return cls(updated_at=make_timestamp())

class SquareCreateCustomer(Mutation):

  customer = Field(SquareCustomerType)

  class Arguments:
    
    customer = SquareCustomerInput(required=True)
    idempotency_key = String()
  
  @classmethod
  def mutate(cls, root, ctx, customer, idempotency_key=None):
    customer = square_merchant.customers.create(
      idempotency_key=idempotency_key,
      **customer
    )
    return cls(customer=customer)

class SquareRemoveGroupFromCustomer(Mutation):

  updated_at = String()

  class Arguments:
    customer_id = ID(required=True)
    group_id = ID(required=True)

  def mutate(root, ctx, customer_id, group_id):
    square_merchant.customers.remove_group_from_customer(
        customer_id,
        group_id
      )
    return SquareRemoveGroupFromCustomer(
      updated_at = make_timestamp()
    )

class SquareAddGroupToCustomer(Mutation):

  updated_at = String()
  
  class Arguments:
    customer_id = ID(required=True)
    group_id = ID(required=True)

  def mutate(root, ctx, customer_id, group_id):
    square_merchant.customers.add_group_to_customer(
        customer_id,
        group_id
      )
    return SquareAddGroupToCustomer(
      updated_at=make_timestamp()
    )