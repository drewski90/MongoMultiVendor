from pydantic import BaseModel
from square.client import Client
from . import graphql

class SquareAPI(BaseModel):

  access_token:str
  environment:str
  application_id:str
  application_secret:str

  def __post__init__(self):
    self.client = Client(
      access_token=self.access_token,
      environment=self.environment
    )
  
