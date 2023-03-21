from graphene import (
  ObjectType,
  InputObjectType,
  String,
  Int
)

class SquareMoneyType(ObjectType):
  amount = Int()
  currency = String()

class SquareMoneyInput(InputObjectType):
  amount = Int(required=True)
  currency = String(required=True)