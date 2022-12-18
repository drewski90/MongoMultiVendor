from graphene import (
  Mutation,
  String,
  Field,
  Argument,
  ObjectType,
  InputObjectType
)
from ....sessions import current_user
from graphene import (
  InputObjectType,
)

class AddressInputType(InputObjectType):
  line_1 = String()
  line_2 = String()
  city = String()
  state = String()
  country = String()
  postal_code = String(required=True)

class CreateCardInputType(InputObjectType):
  source = String(required=True)
  cardholder_name = String()
  address = Field(AddressInputType)

# class CreatePaymentMethod(Mutation):

#   payment_method = Field(PaymentMethod)

#   class Arguments:
#     processor = Argument(PaymentProcessors, required=True)
#     card = CreateCardInputType(required=False)
#     type = Argument(PaymentMethodTypes, required=True)
#     idempotency_key = String(required=True)

#   def mutate(root, ctx, processor, **kwargs):
#     pp = get_processor(processor)
#     result = pp.payment_methods.create(current_user, **kwargs)
#     return CreatePaymentMethod(payment_method=result)

# class SquareMutations(ObjectType):
#   create_payment_method = CreatePaymentMethod.Field()