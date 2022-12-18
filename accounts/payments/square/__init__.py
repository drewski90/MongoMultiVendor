from .document import Square
from square.client import Client
from ...webhooks import Webhook
from .scopes import scopes
from ...utils import ensure_https
from ...sessions import account_loaded, current_org, current_user
from flask import request, current_app
from datetime import datetime
from ...graphql import Graph
from .helpers import get_credentials, authorization_url
from graphene import ObjectType, List, Argument, String, Int, Mutation
from graphene.types.generic import GenericScalar
from .helpers import make_date_range, square_merchant
from ...organizations import Organization

class SquarePayments:

  def __init__(self, flask_app):
    
    self.flask_app = flask_app
    credentials = get_credentials(flask_app)
    self.client = Client(
      access_token=credentials['access_token'],
      environment=credentials['environment']
    )
    self.create_webhooks()
    Graph.add_query(SquareQueries)

  @classmethod
  def create_webhooks(cls):
    cls.oauth_hook = Webhook(
      "square_oauth", 
      cls.handle_auth_code
    )

  @classmethod
  def handle_auth_code(cls):

    try:
      credentials = get_credentials(current_app)

      client = Client(
        access_token=credentials['access_token'],
        environment=credentials['environment']
      )

      body = {
        "client_id": credentials['application_id'],
        "grant_type": "authorization_code",
        "client_secret": credentials['application_secret'],
        "code": request.args['code'],
        "code_verifier": None,
        "redirect_uri": ensure_https(cls.oauth_hook.url()),
        "refresh_token": None,
        "scopes": scopes,
        "short_lived": None
      }

      result = client.o_auth.obtain_token(body=body)

      if result.is_error():
        raise Exception(str(result.errors))

      body = result.body
      if 'expires_at' in body:
        body['expiration'] = datetime.strptime(
            body.pop('expires_at'),
            '%Y-%d-%mT%H:%M:%SZ'
          )

      org = Organization.objects.get(id=request.args['state'])

      square = Square(processor='square', **body)
      org.payment_processors = [
        i for i in org.payment_processors or []
        if not isinstance(i, Square)
      ]
      org.payment_processors.append(square)
      org.save()

      return "Access saved"
    except:
      return "Error occurred, please try again"

class SquareQueries(ObjectType):

  square_authorization_url = String()

  def resolve_square_authorization_url(r, c):
    credentials = get_credentials(current_app)
    return authorization_url(
      client_id=credentials['application_id'],
      scope = scopes,
      state=current_org.id,
      redirect_uri=SquarePayments.oauth_hook.url()
    )


__all__ = [
  "Square",
  "Square"
]
