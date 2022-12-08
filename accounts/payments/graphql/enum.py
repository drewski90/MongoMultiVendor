from graphene import Enum

class PaymentProcessors(Enum):
  square = 'square'

class PaymentMethodTypes(Enum):
  card = "card"