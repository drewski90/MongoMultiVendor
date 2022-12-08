from square.client import Client
from ...utils import populate_document
from datetime import datetime, timedelta, timezone
import dateutil.parser
from .helpers import get_credentials
from flask import current_app
from ...sessions import current_org
from uuid import uuid4
from mongoengine import (
  EmbeddedDocument,
  StringField,
  DateTimeField,
  BooleanField
)

class SquareClient:

  "works as a property to square"

  def renew_token(self, obj):
    credentials = get_credentials(current_app)
    client = Client(
      access_token=credentials['access_token'],
      environment=credentials['environment']
    )
    client_id = credentials['application_id']
    body = {
      "client_id": client_id,
      "grant_type": "refresh_token",
      "client_secret": credentials['application_secret'],
      "refresh_token": obj.refresh_token
    }
    result = client.o_auth.obtain_token(body=body)
    if result.is_success():
      body = result.body
      if 'expires_at' in body:
        expiration = datetime.strptime(
          body.pop('expires_at'),
          "%Y-%m-%dT%H:%M:%SZ"
        )
        body['expiration'] = expiration
      populate_document(obj, body)
      current_org.save()
    else:
      raise Exception(result.errors)

  def __get__(self, obj, objtype=None):
    if client := getattr(obj, '_client', None):
      return client
    if obj.access_token:
      if datetime.utcnow() >= obj.expiration:
        self.renew_token(obj)
      client = Client(access_token=obj.access_token)
      obj._client = client
      return client

def error_handler(api_response):
  if api_response.is_success():
    return api_response.body
  elif api_response.is_error():
    print(api_response.errors[0])
    raise Exception(api_response.errors[0]['detail'])

class SquareLocations:

  def __init__(self, parent):
    self.parent = parent

  @property
  def api(self):
    return self.parent.client.locations

  def get(self, id):
    return error_handler(
      self.api.retrieve_location(id)
    )['location']

  def list(self):
    return error_handler(
      self.api.list_locations()
    )['locations']

class SquareBookings:

  def __init__(self, parent):
    self.parent = parent

  @property
  def api(self):
    return self.parent.client.bookings

  def list(
      self, 
      location_id=None, 
      team_member_id=None,
      cursor=None,
      limit=None,
      start_at_min=None,
      start_at_max=None
    ):
    body = {}
    if location_id:
      body['location_id'] = location_id
    if team_member_id:
      body['team_member_id'] = team_member_id
    if cursor:
      cursor['cursor'] = cursor
    if limit:
      body['limit'] = limit
    if start_at_min:
      body['start_at_min'] = start_at_min
    if start_at_max:
      body['start_at_max'] = start_at_max
    result = self.api.list_bookings(body)
    return error_handler(result)['bookings']

  def create(self, user=None):
    return 
    
  
  def avaliability(
    self, 
    location_id, 
    service_variation_ids, 
    start_date=None, 
    team_member_ids=None
  ):
    body = {}
    body['query'] = {}
    body['query']['filter'] = {}
    if start_date:
      date = dateutil.parser.isoparse(start_date)
    else:
      date = datetime.now(timezone.utc).astimezone() + timedelta(days=1)
    body['query']['filter']['start_at_range'] = {
      "start_at": date.isoformat('T'),
      "end_at": (date + timedelta(days=1)).isoformat("T")
    }
    body['query']['filter']['location_id'] = location_id
    seg_filts = []
    for variation_id in service_variation_ids:
      _filter = {"service_variation_id": variation_id}
      if team_member_ids:
        _filter['team_member_id_filter'] = {"any":team_member_ids}
      seg_filts.append(_filter)
    body['query']['filter']['segment_filters'] = seg_filts
    result = self.api.search_availability(body)

    return error_handler(
      result
    )['availabilities']

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


class SquareCatalog:

  def __init__(self, parent):
    self.parent = parent
  
  @property
  def api(self):
    return self.parent.client.catalog

  def list(self, types=[
    "ITEM",
    "IMAGE",
    "CATEGORY",
    "TAX", 
    "DISCOUNT", 
    "MODIFIER_LIST",
    "PRICING_RULE", 
    "PRODUCT_SET", 
    "TIME_PERIOD", 
    "MEASUREMENT_UNIT",
    "SUBSCRIPTION_PLAN", 
    "ITEM_OPTION", 
    "CUSTOM_ATTRIBUTE_DEFINITION",
    "IMAGE"
  ]):
    result = error_handler(
      self.api.list_catalog(
        types=','.join(types)
      )
    )
    if 'cursor' not in result:
      return result['objects']
    if 'cursor' in result:
      output = result['objects']
      while 'cursor' in result:
        result = error_handler(
          self.api.list_catalog(
            cursor=result['cursor'],
            types=','.join(types)
          )
        )
        output += result['objects']
      return output

class SquareTeams:
  def __init__(self, parent):
    self.parent = parent
  
  @property
  def api(self):
    return self.parent.client.team

  def list(self, locations=None):
    body = {}
    body['query'] = {}
    body['query']['filter'] = {}
    if locations:
      body['query']['filter']['location_ids'] = locations
    body['query']['filter']['status'] = 'ACTIVE'
    result = self.api.search_team_members(body)
    return error_handler(result)['team_members']


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

class SquareModel:
  
  def __init__(self, module):
    self.module = module
  
  def __get__(self, obj, objtype=None):
    return self.module(obj)

class Square(EmbeddedDocument):

  processor = StringField(max_length=90)
  merchant_id = StringField(max_length=90)
  access_token = StringField(max_length=255)
  refresh_token = StringField(max_length=255)
  token_type = StringField(max_length=255)
  short_lived = BooleanField(max_length=255)
  expiration = DateTimeField()

  client = SquareClient()
  team = SquareModel(SquareTeams)
  catalog = SquareModel(SquareCatalog)
  locations = SquareModel(SquareLocations)
  bookings = SquareModel(SquareBookings)
  payment_methods = SquareModel(SquarePaymentMethods)
  customers = SquareModel(SquareCustomers)

  def get_customer_id(self, user):
    return self.customers.retrieve(user)['id']

  def __repr__(self):
    return self.__class__.__name__

  def __str__(self):
    return self.__class__.__name__