from datetime import timedelta, datetime, timezone
from ...utils import ensure_https
from urllib.parse import quote
from werkzeug.local import LocalProxy
from ...sessions import current_org

def make_date_range(
  start_ts=None, 
  end_ts=None, 
  max_range=timedelta(days=32), 
  min_range=timedelta(days=1)
  ):
  if start_ts:
    start = datetime.utcfromtimestamp(start_ts).astimezone()
  else:
    start = datetime.now(timezone.utc).astimezone()
  if end_ts:
    end = datetime.utcfromtimestamp(end_ts).astimezone()
  else:
    end = start + timedelta(days=1)
  assert start < end, "End date is less than start date"
  assert end - start <= max_range, f"Range is too long {end-start}"
  assert end - start >= min_range, f"Range is too short {end-start}"
  return start.isoformat('T'), end.isoformat('T')

CREDENTIALS = None

def get_credentials(app):
  global CREDENTIALS
  if CREDENTIALS is None:
    config = app.config['SQUARE']
    mode = config['mode']
    CREDENTIALS = dict(
      environment = mode,
      access_token = config[mode]['access_token'],
      application_secret = config[mode]['application_secret'],
      application_id=config['application_id']
    )
  return CREDENTIALS    
