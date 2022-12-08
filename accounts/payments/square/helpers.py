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

def authorization_url(client_id, state=None, redirect_uri=None, scope=[]):
  params = {
    "client_id": client_id,
    "session": 'true',
    "redirect_uri": quote(ensure_https(redirect_uri)),
    "scope": scope if isinstance(scope, str) else '+'.join(scope).upper(),
    "state": str(state)
  }
  params_string = "&".join([k + '=' + v for k, v in params.items()])
  return f"https://connect.squareup.com/oauth2/authorize?{params_string}"

def get_square():
  test = lambda item: item.processor == 'square'
  square = next(filter(test, current_org.payment_processors), None)
  if square:
    return square
  raise Exception(f"There is no square account configured for {current_org.name}")

square_merchant = LocalProxy(get_square)


def address_to_square(user, address):
  return {
    "first_name": user.first_name,
    "last_name": user.last_name,
    "address_line_1": address.line_1,
    "address_line_2": address.line_2,
    "locality": address.city,
    "administrative_district_level_1": address.state,
    "administrative_district_level_2": address.country,
    "postal_code": address.postal_code,
    "country": address.country
  }