from typing import Any
from pydantic import (
  BaseModel, 
  Field,
  Extra,
  validate_model
)

class Model(BaseModel):

  class Config:
    validate_assignment = True
    use_enum_values = True
    exta = Extra.forbid
    allow_arbitrary_values=False

class APIModel(Model):

  api_wrapper:Any = Field(
    repr=False, 
    exclude=True
  )

  @property
  def merchant(self):
    return self.api_wrapper.merchant

  @property
  def client(self):
    return self.merchant.client

  @property
  def api(self):
    return self.api_wrapper.api

  @property
  def update_fields(self):
    data = self.dict(
      include=self._edit_fields_,
      exclude_unset=True,
      exclude_none=True
    )
    if 'api_wrapper' in data:
      data.pop('api_wrapper')
    return data

  def refresh(self, **data):
    """Refresh the internal attributes with new data."""
    values, fields, error = validate_model(self.__class__, data)
    if error:
      raise error
    for name in fields:
      value = values[name]
      setattr(self, name, value)
    return self

class APIWrapper:

  def __init__(self, merchant):
    assert merchant is not None
    self.merchant = merchant

  class NotImplemented(Exception):
    pass

  @property
  def api(self):
    return getattr(
      self.merchant.client, 
      self.api_name
    )

  def list(self):
    raise NotImplemented()

  def retrieve(self):
    raise NotImplemented()
  
  def update(self):
    raise NotImplemented()

  def delete(self):
    raise NotImplemented()

