from mongoengine.base.common import _document_registry
from .media import install_media
from .apis.square import SquareAPI
import importlib
from .admin import Admin
from .graphql import Graph
from .webhooks import Webhooks
from flask_babelex import Babel
from flask import request, session
from uuid import uuid4
from .utils import pascal_to_snake
import atexit
from mongoengine import connect
from pymongo import MongoClient

class App:

  def close_db(self):
    for db in self._db_clients:
      db.close()

  def open_db(self, db):
    self._db_clients = []
    if not isinstance(db, (list, tuple)):
      db = [db]
    for _db in db:
      if isinstance(_db, MongoClient):
        self._db_clients.append(_db)
      if isinstance(_db, dict):
        name = _db.pop('db')
        conn = connect(name, **_db)
        self._db_clients.append(conn)
      else:
        raise (f"Database config invalid at {_db}")
    atexit.register(self.close_db)

  def __init__(
    self, 
    flask_app,
    db=None,
    app_name="App",
    organizations=False
    ):

    self.app_name = app_name
    self.flask_app = flask_app
    if db:
      self.open_db(db)
    self.users = importlib.import_module(f"{__name__}.users")
    if organizations:
      self.organizations = importlib.import_module(f"{__name__}.organizations")
    babel = Babel(flask_app)
    babel.localeselector(self.get_locale)
    config = flask_app.config['SQUARE']
    mode = config['mode']
    self.square = SquareAPI(
      environment="production",
      access_token=config[mode]['access_token'],
      application_secret=config[mode]['application_secret'],
      application_id=config['application_id']
    )
    install_media(flask_app)
    self.initialize_app()

  def ensure_session_id(self):
    if not 'id' in session:
      session['id'] = str(uuid4())[:8]

  def initialize_app(self):

    self.flask_app.before_request(
      self.ensure_session_id
    )
    
    self.admin = Admin(
      self.flask_app,
      name=self.app_name,
      template_mode='bootstrap4',
      url="/admin/"
    )

    self.graphql = Graph(
      self.flask_app, 
      "/graphql/", 
      "graphql"
    )

    self.webhooks = Webhooks(
      self.flask_app
    )
    # instead of converting model names to snake case
    # set it as a static property on all registered docs
    for model in _document_registry.values():
      model.__snakename__ = pascal_to_snake(model.__name__)

  def get_locale(self):
    if 'lang' in request.args:
      session['lang'] = request.args.get('lang', 'en')
    return session.get('lang', 'en')
    


