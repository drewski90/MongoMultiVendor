from .errors import error_handler

class SquareCustomers:

  def __init__(self, parent):
    self.parent = parent
  
  @property
  def api(self):
    return self.parent.client.customers

  def format_customer_data(self, user):
    body = {}
    body['given_name'] = user.first_name
    body['family_name'] = user.last_name
    body['email_address'] = user.email
    if addr := getattr(user, 'address', None):
      body['address'] = {}
      body['address']['address_line_1'] = addr.line_1
      body['address']['address_line_2'] = addr.line_2
      body['address']['locality'] = addr.city
      body['address']['administrative_district_level_1'] = addr.state
      body['address']['postal_code'] = addr.postal_code
      body['address']['country'] = addr.country
    body['phone_number'] = user.phone_number
    body['customer_id'] = str(user.id)
    return body

  def create(self, user):
    body = self.format_customer_data(user)
    return error_handler(
      self.api.create_customer(
      body=body
      )
    ).get('customer')

  def update(self, user):
    customer = self.retrieve(user)
    return error_handler(
      self.api.update_user(
        customer_id = customer['id'],
        body=self.format_customer_data(user)
      )
    ).get('customers')[0]

  def retrieve(self, user):
    body = {}
    body['limit'] = 1
    body['query'] = {}
    body['query']['filter'] = {}
    body['query']['filter']['email_address'] = {}
    body['query']['filter']['email_address']['fuzzy'] = user.email
    result = self.api.search_customers(body=body)
    if "customers" not in result.body or len(result.body['customers']) == 0:
      return self.create(user)
    else:
      return error_handler(result)['customers'][0]


