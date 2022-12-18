from .errors import error_handler

class SquarePaymentMethods:
  def __init__(self, parent):
    self.parent = parent
    
  @property
  def api(self):
    return self.parent.client.cards

  def list(self, user):
    return error_handler(self.api.list_cards(
      reference_id = str(user.id)
    ))['cards']

  def create(self, user, card, idempotency_key, **kwargs):
    source = card['source']
    address = card['address']
    card_holder = card['cardholder_name']
    body = {}
    body['idempotency_key'] = idempotency_key
    body['source_id'] = source
    body['card'] = {}
    body['card']['cardholder_name'] = card_holder
    body['card']['billing_address'] = {}
    body['card']['billing_address']['address_line_1'] = address.line_1
    body['card']['billing_address']['address_line_2'] = address.line_2
    body['card']['billing_address']['locality'] = address.city
    body['card']['billing_address']['administrative_district_level_1'] = address.state
    body['card']['billing_address']['postal_code'] = address.postal_code
    body['card']['billing_address']['country'] = address.country
    body['card']['customer_id'] = self.parent.get_customer_id(user)
    return error_handler(
      self.api.create_card(body=body)
    )['card']

  def list(self, user):
    return error_handler(
      self.api.list_cards(
        reference_id=str(user.id)
      )
    )['cards']