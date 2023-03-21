from mongoengine import ValidationError, NotUniqueError
from .scalars import ObjectId
from .model_input_type import generate_model_input_type
from ..utils import populate_document, pascal_to_snake
from inspect import isclass
from graphene.types.generic import GenericScalar
from graphene import (
  ObjectType,
  InputObjectType,
  Mutation,
  Field,
  List,
  Int,
  String,
  Argument,
  Scalar
)

# graph object imports all views registered
REGISTRY = []

def generate_mutation(name, arguments, resolver_function, return_fields):
  mutation_attrs = {
    "Arguments": type("Arguments", (object, ), arguments),
    "mutate": resolver_function,
  }
  mutation_attrs.update(return_fields)
  return type(name, (Mutation, ), mutation_attrs)

class PaginationOptionsInputType(InputObjectType):
  page = Int()
  limit = Int()
  sort_by = String()

class FilterInputType(GenericScalar):
  pass

class GQLModelSchemaMetaclass(type):

  def __new__(cls, name, bases, attrs):

    new_cls = super().__new__(cls, name, bases, attrs)

    if getattr(new_cls, 'model', None) is None:
      return new_cls

    is_accessible = getattr(new_cls, 'is_accessible', None)
    if is_accessible is None:
      print('\033[91m', f"{name} has no 'is_accessible' method, will always return False",'\033[0m')
      new_cls.is_accessible = lambda *args, **kwargs: False
    new_cls.is_accessible = classmethod(is_accessible)

    REGISTRY.append(new_cls)
    model = getattr(new_cls, 'model')
    if 'secured_objects' not in dir(model):
      print('\033[96m', f"{model.__name__} does not implement a 'secured_objects' method",'\033[0m')
    model_name = pascal_to_snake(model.__name__)
    object_type = getattr(new_cls, 'object_type')

    # generate mutations for CUD operations

    mutations = {
      k:v.Field() for k,v in attrs.items() \
        if isclass(v) and issubclass(v, Mutation)
    }

    if getattr(new_cls, 'can_create', False):

      fields = getattr(new_cls, 'create_fields', None) or []

      if len(fields) == 0:
        fields.append('*')

      if '-id' not in fields:
        fields.append('-id')

      input_type = generate_model_input_type(model, fields, type_prefix="Create")

      mutation = generate_mutation(
        f"Create{model.__name__}",
        {model_name: input_type(required=True)},
        getattr(new_cls, 'create'),
        {model_name: Field(object_type)}
      ).Field()

      mutations[f"create_{model_name}"] = mutation

    if getattr(new_cls, 'can_update', False):

      fields = getattr(new_cls, 'update_fields', None) or []

      if len(fields) == 0:
        fields.append('*')

      if '!id' not in fields:
        fields.append('!id')
      
      if '-id' in fields:
        fields.remove('-id')

      input_type = generate_model_input_type(model, fields, type_prefix="Update")

      mutation = generate_mutation(
        f"Update{model.__name__}",
        {model_name: input_type(required=True)},
        new_cls.update,
        {model_name: Field(object_type)}
      ).Field()

      mutations[f"update_{model_name}"] = mutation

    if getattr(new_cls, 'can_delete', False):

      mutations[f"delete_{model_name}"] = generate_mutation(
        f"Delete{model.__name__}",
        {"id": ObjectId(required=True)},
        getattr(new_cls, 'delete', None),
        {"id": ObjectId()}
      ).Field()

    mutation_class = type(
        f"{model.__name__}Mutations",
        (ObjectType,),
        mutations
      )

    setattr(new_cls, 'mutation_class', mutation_class)

    # create query class

    if getattr(new_cls, 'can_read', None):

      paginator = type(
        f"{model.__name__}Pagination",
        (ObjectType,),
        {
          "results": List(object_type),
          "resolve_results": lambda r, c: r,
          "count": Int(),
          "resolve_count": lambda r, c: r.count()
        }
      )

      if plural:=getattr(new_cls, 'verbose_name_plural', None):

        plural.replace(' ', '_')
        q_name = plural

      else:

        q_name = model_name + 's'

      query_fields = {}

      for k, v in attrs.items():

        if isinstance(v, (List, Scalar, Argument, Field)):

          query_fields[k] = v

          query_fields[f"resolve_{k}"] = getattr(
            new_cls, 
            "resolve_" + k
          )

      query_fields[q_name] = Field(
        paginator,
        options=Argument(PaginationOptionsInputType),
        filter=Argument(FilterInputType)
      )

      query_fields[f"resolve_{q_name}"] = getattr(
        new_cls, 
        'get_list', 
        None
      )

      
      query_class = type(
        f"{model.__name__}Queries",
        (ObjectType,),
        query_fields
      )

      setattr(
        new_cls, 
        'query_class', 
        query_class
      )

    return new_cls


class GQLModelSchema(metaclass=GQLModelSchemaMetaclass):
  
  model = None
  object_type = None
  can_create = True
  create_fields = None
  can_read = True
  can_update = True
  update_fields = None
  can_delete = True
  filters = None
  verbose_name_plural=None
  page_size = 20

  @classmethod
  def get_query(cls):
    if hasattr(cls.model, 'secured_objects'):
      return cls.model.secured_objects()
    return cls.model.objects

  @classmethod
  def assert_permission(cls, action):
    assert cls.is_accessible(action), \
      f"You do not have access to {action} " \
      f"{cls.model.__snakename__.replace('_', ' ')}"

  @classmethod
  def get_list(cls, root, ctx, options=None, filter=None):

    page_size = min(cls.page_size, 30)
    page = 1

    query = cls.get_query()

    if filter:
      query = query.filter(**filter)

    if options:
      if sort_by:=options.get('sort_by'):
          query = query.order_by(sort_by)
      if "limit" in options:
        page_size = options['limit']
      if "page" in options:
        page = options['page']

    query = query.limit(page_size)

    if page and page_size:
        query = query.skip((page * page_size) - page_size)

    return query

  @classmethod
  def get_one(cls, id):
    try:
      instance = cls.get_query().filter(pk=id).first()
      if not instance:
        raise Exception('Document not found')
      return instance
    except ValidationError as e:
      raise Exception('Validation error')

  @classmethod
  def create(cls, root, ctx, **kwargs):
    cls.assert_permission('create')
    instance = cls.model(**kwargs[cls.model.__snakename__])
    cls.on_create(instance, **kwargs)
    if not instance.pk:
      try:
        instance.save(validate=True)
      except Exception as ex:
        raise Exception(f'Save error occurred ({str(ex.__class__.__name__)})')
    return {cls.model.__snakename__: instance}

  @classmethod
  def on_create(cls, instance, **kwargs):
    pass

  @classmethod
  def update(cls, root, ctx, **kwargs):
    cls.assert_permission('update')
    data = kwargs[cls.model.__snakename__]
    id = data.pop('id')
    instance = cls.get_one(id)
    populate_document(instance, data)
    changes = getattr(instance, "_changed_fields", [])
    if len(changes) > 0:
      cls.on_update(instance, **kwargs)
      try:
        instance.save(validate=True)
      except NotUniqueError:
        raise Exception('Document could not be updated')
    return {cls.model.__snakename__: instance}

  @classmethod
  def on_update(cls, instance, **kwargs):
    pass

  @classmethod
  def delete(cls, root, ctx, id):
    cls.assert_permission('delete')
    instance = cls.get_one(id)
    cls.before_delete(instance)
    instance.delete()
    return {"id": id}

  @classmethod
  def before_delete(cls, instance):
    pass
