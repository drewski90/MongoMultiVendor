from .errors import error_handler
from datetime import datetime, timedelta, timezone
import dateutil.parser

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
    
  
  def availability(
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