from dataclasses import dataclass
from square.client import Client
from ...webhooks import Webhook
from ...graphql import Graph
from .graphql import SquareQueries
from .models import SquareOAuth
from flask import request
from .scope import scope
from datetime import datetime
from ...utils import ensure_https
from urllib.parse import quote

@dataclass(init=True)
class SquareAPI:

  access_token:str
  environment:str
  application_id:str
  application_secret:str

  def __post_init__(self):
    # add reference to this instance
    SquareOAuth.square = self
    self.authorization_hook = Webhook(
      "square_oauth_authorization",
      self.handle_oauth_code
    )
    Graph.add(query=SquareQueries)

  @property
  def client(self):
    return Client(
      access_token=self.access_token,
      environment=self.environment
    )

  def handle_oauth_code(self):

    if 'code' in request.args and 'state' in request.args:
      try:
        token_data = self.obtain_token(
          code=request['code'],
          state=request['state']
        )
        print(token_data)
        return "Square authorization has been saved"
      except:
        return "Token could not be obtained", 500
    else:
      return "Invalid request", 500

  def generate_oauth_uri(self, state):
    params = {
      "client_id": self.application_id,
      "session": 'true',
      "redirect_uri": quote(ensure_https(self.authorization_hook.url())),
      "scope": scope if isinstance(scope, str) else '+'.join(scope).upper(),
      "state": str(state)
    }
    params_string = "&".join([k + '=' + v for k, v in params.items()])
    return f"https://connect.squareup.com/oauth2/authorize?{params_string}"

  def obtain_token(self, code):

    result = self.client.oauth.obtain_token(
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