from .utils import APIModel, APIWrapper
from urllib.parse import quote
from datetime import datetime

scope = set(
  [
  "APPOINTMENTS_WRITE",
  "APPOINTMENTS_READ",
  "APPOINTMENTS_BUSINESS_SETTINGS_READ",
  "PAYMENTS_READ",
  "PAYMENTS_WRITE",
  "ITEMS_WRITE",
  "ITEMS_READ",
  "ORDERS_WRITE",
  "ORDERS_READ",
  "PAYMENTS_WRITE",
  "CUSTOMERS_READ",
  "CUSTOMERS_WRITE",
  "EMPLOYEES_READ",
  "GIFTCARDS_READ",
  "GIFTCARDS_WRITE",
  "INVOICES_READ",
  "INVOICES_WRITE",
  "ORDERS_WRITE",
  "ORDERS_READ",
  "TIMECARDS_SETTINGS_READ",
  "TIMECARDS_SETTINGS_WRITE",
  "TIMECARDS_WRITE",
  "TIMECARDS_READ",
  "PAYOUTS_READ",
  "SUBSCRIPTIONS_WRITE",
  "SUBSCRIPTIONS_READ",
  "MERCHANT_PROFILE_READ",
  "MERCHANT_PROFILE_WRITE"
  ]
)

def https_only_string(uri):
  if not uri.startswith("https://"):
    split = uri.split('://')
    if len(split) == 1:
      uri = "https://" + uri
    elif len(split) <= 2:
      split[0] = "https"
      uri = "://".join(split)
  return uri

class Oauth(APIWrapper):
  api_name = "oauth"

  def handle_oauth_code(self, request):
    if 'code' in request.args and 'state' in request.args:
      try:
        return self.obtain_token(
          code=request['code'],
          state=request['state']
        )
        return "Square authorization has been saved"
      except:
        return "Token could not be obtained", 500
    else:
      return "Invalid request", 500

  def oauth_uri(self, state, callback_uri):
    params = {
      "client_id": self.merchant.application_id,
      "session": 'true',
      "redirect_uri": quote(https_only_string(callback_uri)),
      "scope": scope if isinstance(scope, str) else '+'.join(scope).upper(),
      "state": str(state)
    }
    params_string = "&".join([k + '=' + v for k, v in params.items()])
    return f"https://connect.squareup.com/oauth2/authorize?{params_string}"

  def obtain_token(self, code):

    result = self.api.obtain_token(
      body=dict(
        client_id=self.application_id,
        client_secret=self.application_secret,
        grant_type="authorization_code",
        code=code,
        code_verifier=None,
        scopes=scope,
        short_lived=None
      )
    )

    if result.is_error():
      raise Exception(str(result.errors))

    body = result.body

    # convert expiration date to usable date
    if 'expires_at' in body:
      body['expiration'] = datetime.strptime(
          body.pop('expires_at'),
          '%Y-%d-%mT%H:%M:%SZ'
        )
    
    return body

