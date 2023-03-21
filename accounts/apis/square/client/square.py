from square.client import Client
from .cards import Cards
from .customers import Customers
from .customer_groups import CustomerGroups
from .locations import Locations
from .merchants import Merchant, Merchants
from .team import TeamMembers
from .booking import Bookings
from .catalog import Catalog
from .payments import Payments
from .oauth import Oauth

class Merchant:

  def __init__(
      self, 
      access_token, 
      environment="production",
      application_id=None
    ):
    self.application_id = application_id
    self.client = Client(
      access_token=access_token,
      environment=environment
    )

  @property
  def catalog(self):
    return Catalog(self)

  @property
  def cards(self):
    return Cards(self)

  @property
  def customers(self):
    return Customers(self)

  @property
  def locations(self):
    return Locations(self)

  @property
  def merchants(self):
    return Merchants(self)

  @property
  def team(self):
    return TeamMembers(self)

  @property
  def bookings(self):
    return Bookings(self)

  @property
  def customer_groups(self):
    return CustomerGroups(self)

  @property
  def payments(self):
    return Payments(self)

  @property
  def oauth(self):
    return Oauth(self)

class Square(Merchant):
  pass
