import mongoengine as me
from .scalars import ObjectId, Date
import graphene as gp
from graphene.types.generic import GenericScalar
from pprint import pprint

EMBEDDED_INPUT_TYPE_REGISTRY  = {}
ENUM_REGISTRY = {}
FIELD_CONVERTERS = []

def mongofield_conversion(*types):
  def decorator(func):
    FIELD_CONVERTERS.insert(0, (types, func))
    def wrapper(*args, **kwargs):
      return func(*args, kwargs)
    return wrapper
  return decorator

def parse_fields_config(_fields):

  exclude = ["_cls"]
  required = []
  fields = []
  do_not_require = ['_cls']
  all_fields = False
  require_all = False

  for field in _fields:

    if isinstance(field, str):

      if field == "*":
        all_fields = True
      elif field == "!*":
        all_fields = True
        require_all = True
      elif field.startswith("-"):
        exclude.append(field[1:])
      elif field.startswith('!'):
        required.append(field[1:])
      else:
        do_not_require.append(field)
        fields.append(field)
    
    elif isinstance(field, dict):

      assert 'name' in field , \
        f"{field} doesnt specify the field name"
      if "required" in field:
        if field['required']:
          required.append(field['name'])
        else:
          do_not_require.append(field['name'])
      if "exclude" in field:
        exclude.append(field)

    else:

      raise Exception(
        f"fields config does not support {type(field)} type"
      )

  if (len(fields) + len(required)) == 0:
    all_fields = True

  return {
    "exclude": exclude,
    "do_not_require": do_not_require,
    "required": required,
    "fields": fields,
    "all_fields": all_fields,
    "require_all": require_all
  }

def convert_field(**kwargs):
  expected_output = (
    gp.List,
    gp.Scalar,
    gp.Argument, 
    gp.Field
  )
  if kwargs.get('path') is None:
    kwargs['path'] = ""
  for conversion in FIELD_CONVERTERS:
    types, handler = conversion
    if isinstance(kwargs['field'], types):
      output = handler(**kwargs)
      if isinstance(output, expected_output):
        return output
      raise Exception(
        f"\033[91mfield conversion error: {handler} did not return one"
        f" of {[i.__name__ for i in expected_output]} \033[0m"
        )
  print(
    f"\033[96mNo field converter found for {kwargs['field'].__class__.__name__}"
    " this field will be ignored by default. \n"
    "To specify a new field conversion function, use the "
    f"mongofield_conversion decorator \033[0m"
  )
  

def generate_model_input_type(model, fields, type_prefix=""):

  config = parse_fields_config(fields)

  input_fields = {}

  for name, field in model._fields.items():

    required = any([
      config['require_all'],
      name in config['required']
    ]) and name not in config['do_not_require']

    use_field = any([
        config['all_fields'],
        name in config['fields'],
        required
      ]) and name not in config['exclude']

    if use_field:

      field = convert_field(
        name=name,
        field=field,
        field_config=config,
        required=required,
        type_prefix=type_prefix
      )
      if field:
        input_fields[name] = field

  if len(input_fields) == 0:
    raise Exception(f'No fields at {type_prefix + model.__name__ + "InputType"}')

  input_type = type(
    type_prefix + model.__name__ + "InputType",
    (gp.InputObjectType,), 
    input_fields
  )

  return input_type


@mongofield_conversion(me.IntField, me.LongField)
def to_int(required, **kwargs):
  return gp.Int(required=required)

@mongofield_conversion(
  me.ReferenceField, 
  me.LazyReferenceField, 
  me.GenericReferenceField, 
  me.GenericLazyReferenceField,
  me.CachedReferenceField,
  me.ObjectIdField
  )
def to_object_id(required, **kwargs):
  return ObjectId(required=required)

@mongofield_conversion(
  me.DateTimeField, 
  me.ComplexDateTimeField
)
def to_date(required, **kwargs):
  return gp.DateTime(
    required=required, 
    datetime_input=gp.DateTime(
      required=required
    )
  )

@mongofield_conversion(
  me.DynamicField,
  me.DictField, 
  me.MapField,
  me.GenericEmbeddedDocumentField
)
def to_generic_type(required, **kwargs):
  return GenericScalar(required=required)

@mongofield_conversion(
  me.IntField, 
  me.LongField
)
def to_int(required, **kwargs):
  return gp.Int(required=required)

@mongofield_conversion(me.FloatField)
def to_float(required, **kwargs):
  return gp.Float(required=required)
  

@mongofield_conversion(
  me.EmbeddedDocumentField
)
def generate_embedded_doc_input_type(
    name, 
    field, 
    required,
    field_config, 
    path, 
    type_prefix
  ):

  path = name if len(path) == 0 else f"{path}.{name}"

  embedded_doc = field.document_type

  input_type_name = type_prefix + embedded_doc.__name__ + "InputType"

  if input_type_name in EMBEDDED_INPUT_TYPE_REGISTRY:

    return gp.Field(
      EMBEDDED_INPUT_TYPE_REGISTRY[input_type_name], 
      required=required
    )

  input_fields = {}

  for name, field in embedded_doc._fields.items():

    full_name = f"{path}.{name}"

    is_required = any([
      field_config['require_all'],
      full_name in field_config['required']
    ]) and full_name not in field_config['do_not_require']

    use_field = any([
        field_config['all_fields'],
        full_name in field_config['fields'],
        is_required
      ]) and full_name not in field_config['exclude']

    if use_field:

      input_fields[name] = convert_field(
        name=name,
        field=field,
        field_config=field_config,
        required=is_required,
        path=path,
        type_prefix=type_prefix
      )

  
  input_type = type(
    input_type_name, 
    (gp.InputObjectType,), 
    input_fields
  )

  EMBEDDED_INPUT_TYPE_REGISTRY[input_type_name] = input_type

  return gp.Field(
    input_type, 
    required=required
  )


@mongofield_conversion(
  me.ListField, 
  me.SortedListField
)
def to_list(name, field, field_config, required, path, type_prefix):

  field = convert_field(
    name=name,
    field=field.field,
    field_config=field_config,
    path=path,
    type_prefix=type_prefix,
    required=False
    )
  
  if isinstance(field, gp.Field):
    field = field._type
  else:
    field = field.__class__

  return gp.List(
    field, 
    required=required
  )

@mongofield_conversion(me.BooleanField)
def to_boolean(required, **kwargs):
  return gp.Boolean(required=required)

@mongofield_conversion(
  me.StringField, 
  me.URLField, 
  me.EmailField, 
  me.EnumField
)
def to_string(field, name, required, **kwargs):

  if field.choices:

    name = name.replace('_', '').title()
    if name in ENUM_REGISTRY:
      return ENUM_REGISTRY[name]
    choices = [(i.replace(" ", "_"), i.replace(" ", "_")) for i in field.choices]
    field = gp.Argument(gp.Enum(name, choices), required=required)
    ENUM_REGISTRY[name] = field
    return field

  return gp.String(required=required)
