from graphene import ObjectType, Schema, Interface
from flask_graphql import GraphQLView
from flask import request, session
from inspect import isclass
from .model_schema import REGISTRY

class GraphBuilder:

  def __init__(self):
    self._mutation_classes = []
    self._query_classes = []
    self._type_classes = []

  def add(self, mutation=None, query=None, types=None):
    if mutation:
      self.add_mutation(mutation)
    if query:
      self.add_query(query)
    if types:
      self.add_type(types)
  
  def add_views(self):
    for cls in REGISTRY:
      self.add_type(getattr(cls, 'object_type', None))
      self.add(
        mutation=getattr(cls, 'mutation_class', None),
        query=getattr(cls, 'query_class', None),
      )

  def add_mutation(self, mutation_class):
    assert issubclass(mutation_class, ObjectType), \
      f"{mutation_class} must be a subclass of {ObjectType}"
    self._mutation_classes.append(mutation_class)

  def add_query(self, query_class):
    assert issubclass(query_class, ObjectType), \
      f"{query_class} must be a subclass of {ObjectType}"
    self._query_classes.append(query_class)

  def add_type(self, type):
    assert type is not None, \
      "type is none"
    if isinstance(type, (list, tuple)):
      for t in type:
        self.add_type(t)
    else:
      assert isclass(type) and (
        issubclass(type, ObjectType) or
        issubclass(type, Interface)
      ), \
        f"{type.__name__} must be a subclass of {ObjectType}"
      self._type_classes.append(type)

  @property
  def schema(self):
    if getattr(self, '_schema', None) is not None:
      return self._schema
    self.add_views()
    config = {}
    if len(self._query_classes) > 0:
      config['query'] = type(
        "Queries",
        tuple(self._query_classes),
        {}
      )
    if len(self._mutation_classes) > 0:
      config['mutation'] = type(
        "Mutations",
        tuple(self._mutation_classes),
        {}
      )
    if len(self._type_classes) > 0:
      config['types'] = self._type_classes
    schema = Schema(**config)
    self._schema = schema
    return schema

  @property
  def view(self):
    if view:=getattr(self, '_view', None):
      return view
    view = GraphQLView.as_view(
      'graphql',
      schema=self.schema,
      graphiql=True
    )
    self._view = view
    return view

  def view_function(self, *args, **kwargs):
    result = self.view()
    return result

  def __call__(
      self, 
      flask_app,
      path,
      name,
      **kwargs
    ):

    extentions = flask_app.extensions
    if csrf := extentions.get('csrf'):
      view_func = csrf.exempt(self.view_function)
    else:
      view_func = self.view_function
    
    flask_app.add_url_rule(
      path, 
      name, 
      view_func,
      methods=["POST", "GET"],
      **kwargs
    )

    flask_app.add_url_rule(
      path + "/<organization_id>/", 
      name + "_organization", 
      view_func,
      methods=["POST", "GET"],
      **kwargs
    )

