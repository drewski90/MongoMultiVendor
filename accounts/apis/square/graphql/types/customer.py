from graphene import(
  ID,
  String,
  List,
  Interface,
  ObjectType
)

class SquareCustomerType(Interface):
  id = ID()
  user_id = ID()
  first_name = String()
  last_name = String()
  email = String()
  phone_number = String()
  created = String()
  updated = String()
  # payment_methods = List(PaymentMethod)

  @classmethod
  def resolve_type(cls, instance, info):
    if 'segment_ids' in instance:
      return SquareCustomerType

class SquareCustomerType(ObjectType):
  id = ID()
  user_id = ID()
  first_name = String()
  last_name = String()
  email = String()
  phone_number = String()
  created = String()
  updated = String()
  # payment_methods = List(PaymentMethod)

  def resolve_user_id(r, c):
    return r.get('reference_id')

  # def resolve_payment_methods(r, c):
  #   cards_api = get_square().client.cards
  #   result = cards_api.list_cards(
  #     customer_id=r['id'],
  #     include_disabled=False
  #   )
  #   if result.is_success() and 'cards' in result.body:
  #     return result.body['cards']
  #   elif result.is_error():
  #     print(result.errors)
  #   return []

  def resolve_email(r, c):
    return r['email_address']

  def resolve_created(r, c):
    return r['created_at']

  def resolve_updated(r, c):
    return r['updated_at']
  
  def resolve_first_name(r, c):
    return r['given_name']
  
  def resolve_last_name(r, c):
    return r['family_name']