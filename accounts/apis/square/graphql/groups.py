from graphene import (
  Int,
  List,
  ID,
  String,
  ObjectType,
  Field,
  InputObjectType,
  Mutation
)
from .utils import make_timestamp
from ..client.merchant import square_merchant

class SquareCustomerGroupType(ObjectType):
  id = ID()
  name = String()
  created_at = String()
  updated_at = String()

class SquareCustomerGroupInput(InputObjectType):
  id = ID()
  name = String()
  created_at = String()
  updated_at = String()

class SquareCustomerGroupResults(ObjectType):
  cursor = String()
  groups = List(SquareCustomerGroupType)

class SquareCustomerGroupPaginationInput(InputObjectType):
  limit = Int()
  cursor = String()

class SquareCreateCustomerGroup(Mutation):

  group = Field(SquareCustomerGroupType)

  class Arguments:
    idempotency_key = String(required=True)
    group = SquareCustomerGroupInput(required=True)

  @classmethod
  def mutate(cls, root, ctx, **kwargs):
    group = square_merchant.customer_groups.create(
      **kwargs
    )
    return cls(group=group)

class SquareUpdateCustomerGroup(Mutation):

  group = Field(SquareCustomerGroupType)

  class Arguments:
    idempotency_key = String(required=True)
    group = SquareCustomerGroupInput(required=True)

  @classmethod
  def mutate(cls, root, ctx, **kwargs):
    group = square_merchant.customer_groups.create(
      **kwargs
    )
    return cls(group=group)

class SquareDeleteCustomerGroup(Mutation):

  deleted_at = String()

  class Arguments:
    group_id = ID(required=True)

  @classmethod
  def mutate(cls, root, ctx, group_id):
    square_merchant.customer_groups.delete(
      group_id
    )
    print(make_timestamp())
    print(cls)
    return cls(deleted_at=make_timestamp())