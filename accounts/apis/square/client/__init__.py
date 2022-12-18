"""This module is designed to """
"""wrap the jank that is square's sdk"""

from .bookings import SquareBookings
from .catalog import SquareCatalog
from .locations import SquareLocations
from .customers import SquareCustomers
from .payments import SquarePaymentMethods
from .teams import SquareTeams
from square.client import Client
from ....sessions import current_org, request
from ....utils import populate_document
from datetime import datetime
from flask import current_app

class SquareClient:

  "works as a property to square"

  def renew_token(self, obj):
    client = obj.square.client
    body = {
      "client_id": obj.square.application_id,
      "grant_type": "refresh_token",
      "client_secret": obj.square.application_secret,
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


class SquareDocumentMixin:

  class SquareAPIProperty:
    
    def __init__(self, module):
      self.module = module
    
    def __get__(self, obj, objtype=None):
      return self.module(obj)

  """Mixin for Square EmbeddedDocument"""
  
  client = SquareClient()
  team = SquareAPIProperty(SquareTeams)
  catalog = SquareAPIProperty(SquareCatalog)
  locations = SquareAPIProperty(SquareLocations)
  bookings = SquareAPIProperty(SquareBookings)
  payment_methods = SquareAPIProperty(SquarePaymentMethods)
  customers = SquareAPIProperty(SquareCustomers)

  def get_customer_id(self, user):
    return self.customers.retrieve(user)['id']

  def __repr__(self):
    return self.__class__.__name__

  def __str__(self):
    return self.__class__.__name__