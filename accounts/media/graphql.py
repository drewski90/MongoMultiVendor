from graphene.types.generic import GenericScalar
from mongoengine.base.common import _document_registry as model_registry
from ..sessions import current_user
from ..graphql import MongoType, GQLModelSchema
from .base import Media
from ..graphql import BigInt
from graphene import (
  DateTime,
  InputObjectType,
  Mutation,
  String,
  Int,
  Field,
  Argument,
  Enum
)

MEDIA_MODELS = {}

def get_media_models():
  global MEDIA_MODELS
  if len(MEDIA_MODELS) == 0:
    MEDIA_MODELS = {
      v.__name__:v for k,v in model_registry.items()
      if issubclass(v, Media) and v != Media
    }
  return MEDIA_MODELS

class MediaInputType(InputObjectType):
  file_name = String(required=True)
  content_length = BigInt(required=True)
  content_type = String(required=True)
  access = Argument(
    Enum('access', [
      ('public', 'public'), 
      ('private', 'private')
      ]
    ),
    required=True
  )

class MediaPostInputType(InputObjectType):
  file = Field(MediaInputType, required=True)
  resource = String(required=True)

class GeneratePresignedPost(Mutation):
  link = GenericScalar()

  class Arguments:
    media = MediaPostInputType(required=True)
    
  def mutate(root, ctx, media):
    models = get_media_models()
    model = models.get(media['resource'])
    assert model is not None, \
      f"{media['resource']} does not exist ({list(models.keys())})"
    link = model.generate_presigned_post(**media['file'])
    print("CURRENT USER", current_user)
    return GeneratePresignedPost(link=link)

class MediaType(MongoType):
  file_name = String()
  access = String()
  content_length = Int()
  content_type = String()
  created = DateTime()
  updated = Int()
  url = String()

class MediaModelSchema(GQLModelSchema):
  model = Media
  object_type = MediaType
  verbose_name_plural = "media"
  can_create=False
  update_fields = [
    'file_name',
    'description',
    'access'
  ]

  def is_accessible(cls, action):
    return True
  
  def before_delete(instance):
    assert instance.uploader == current_user \
      or current_user.has_permission('media.delete'), \
        "You dont have permission to delete this object"

  generate_presigned_post = GeneratePresignedPost

