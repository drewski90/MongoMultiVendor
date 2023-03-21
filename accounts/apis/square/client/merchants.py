from dataclasses import dataclass
from .error import request_wrapper

@dataclass
class Merchant:

  country:str
  id:str=None
  business_name:str=None
  language_code:str=None
  currency:str="usd"
  status:str=None
  main_location_id:str=None
  created_at:str=None

class Merchants:

  def __init__(self, merchant):
    self.merchant = merchant
  
  @property
  def client(self):
    return self.merchant.client
  
  @property
  def api(self):
    return self.client.merchants

  def list(self):
    body = request_wrapper(self.api.list_merchants)
    return body['merchant'] if 'merchant' in body else []
