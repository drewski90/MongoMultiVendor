from .errors import error_handler

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
