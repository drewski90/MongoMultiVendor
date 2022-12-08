from .webhooks import Webhooks
from urllib.parse import urlencode
from flask import request

class Webhook:

  def __init__(self, name, callback, methods=['GET']):
    self.installed = False
    self.name = name
    self.methods = methods
    self.path = f"webhooks/{name}/"
    self.callback = callback
    Webhooks.register_webhook(self)

  def install(self, flask_app):
    if self.installed:
      return
    self.flask_app = flask_app
    if "csrf" in flask_app.extensions:
      exempt = flask_app.extensions['csrf'].exempt
      self.callback = exempt(self.callback)
    flask_app.add_url_rule(
      f"/{self.path}",
      f"WebHook:{self.name}",
      self.callback,
      methods=self.methods
    )
    self.installed = True

  @property
  def root_url(self):
    return request.root_url

  @property
  def endpoint(self):
    return self.root_url + self.path

  def url(self, **params):
    query_params = urlencode(params)
    url = self.endpoint
    if len(params) > 0:
      url += "?" + query_params
    return url