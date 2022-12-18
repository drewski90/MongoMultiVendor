from .errors import error_handler

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