from .query import (
  PaymentsQueries,
  SquareCustomerType, 
  SquarePaymentMethodType
)
from .mutation import PaymentsMutations
from ...graphql import Graph

types = (
  SquareCustomerType, 
  SquarePaymentMethodType
)

Graph.add(
  mutation=PaymentsMutations,
  query=PaymentsQueries,
  types=types
)