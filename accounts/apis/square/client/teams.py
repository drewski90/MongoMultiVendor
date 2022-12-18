from .errors import error_handler

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