from square.client import Client
from pydantic import BaseModel

class Address(BaseModel):

  address_line_1:str=None
  address_line_2:str=None
  address_line_3:str=None
  locality:str=None
  sublocality:str=None
  sublocality_2:str=None
  sublocality_3:str=None
  administrative_district_level_1:str=None
  administrative_district_level_2:str=None
  administrative_district_level_3:str=None
  postal_code:str=None
  country:str=None
  first_name:str=None
  last_name:str=None

  @property
  def line_1(self):
    return self.address_line_1

  @line_1.setter
  def line_1(self, value):
    self.address_line_1 = value

  @property
  def line_2(self):
    return self.address_line_2

  @line_2.setter
  def line_2(self, value):
    self.address_line_2 = value

  @property
  def city(self):
    return self.locality

  @city.setter
  def city(self, value):
    self.locality = value

  @property
  def state(self):
    return self.administrative_district_level_1

  @state.setter
  def state(self, value):
    self.administrative_district_level_1 = value
