from graphene import (
  Interface,
  String,
  ObjectType,
)

class Address(Interface):
  line_1 = String()
  line_2 = String()
  city = String()
  state = String() 
  country = String()
  postal_code = String()

  @classmethod
  def resolve_type(cls, instance, info):
      if is_square_address(instance):
          return SquareAddress
      return Address

class AddressType(ObjectType):
  class Meta:
    interfaces = (Address,)

class SquareAddress(ObjectType):
  class Meta:
    interfaces = (Address,)
  
  def resolve_line_1(root, ctx):
    from pprint import pprint
    pprint(root)
    return root['address_line_1']
  
  def resolve_line_2(root, ctx):
    return root['address_line_2']

  def resolve_city(root, ctx):
    return root['locality']

  def resolve_state(root, ctx):
    return root['administrative_district_level_1']

  def resolve_country(root, ctx):
    if res := root.get('administrative_district_level_2'):
      return res
    if res := root.get('country'):
      return res

  def resolve_postal_code(root, ctx):
    return root['postal_code']

def is_square_address(address):
  unique_attributes = [
    "address_line_1",
    'address_line_2',
    'address_line_3',
    'locality',
    'sublocality',
    'sublocality_2',
    'sublocality_3',
    'administrative_district_level_1',
    'administrative_district_level_2',
    'administrative_district_level_3',
    'country',
    'first_name'
    'last_name'
  ]
  for attr in unique_attributes:
    if attr in address:
      return True
  return False


types = (SquareAddress,)