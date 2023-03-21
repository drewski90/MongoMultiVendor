from graphene import (
  String,
  InputObjectType,
  List
)
class SquareTimeRangeInputType(InputObjectType):
  start_at = String()
  end_at = String()

class SquareCustomerTextFilterInput(InputObjectType):
  fuzzy = String()
  exact = String()

class SquareFilterValueInput(InputObjectType):
  all = List(String)
  any = List(String)
  none = List(String)

class SquareFloatNumberRange(InputObjectType):
  start_at = String()
  end_at = String()