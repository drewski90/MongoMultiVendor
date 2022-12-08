from . import crypto
from datetime import datetime
from .utils import format_byte_length
from ..sessions import current_user
from flask import url_for, request
from mongoengine import (
  DynamicDocument,
  DateTimeField,
  ReferenceField,
  StringField,
  IntField,
  queryset_manager,
  Q
)

file_access_options = [
  "public", # allow publilc to list this , 
  "authenticated_read", # allow view if user is authenticated
  'private' # only viewable  from a user account or parent resource
]

class Media(DynamicDocument):

  content_length_range = [1, 16_777_216]
  uri_expiration = 60 * 60

  meta = {
    "collection": "account_media",
    "allow_inheritance": True,
    "indexes": ["access"]
  }
  uploader = ReferenceField("User", null=True)
  file_name = StringField(max_length=1000)
  description = StringField(max_length=1000)
  content_type = StringField(max_length=255, null=False)
  content_length = IntField(min=0, required=True)
  access = StringField(choices=file_access_options, default='private')
  created = DateTimeField(default=datetime.utcnow, required=True)
  updated = DateTimeField(default=datetime.utcnow, required=True)
  last_accessed = DateTimeField(default=datetime.utcnow, required=True)

  def save(self, *args, **kwargs):
    self.updated = datetime.utcnow()
    return super(Media, self).save(*args, **kwargs)

  @property
  def file_size(self):
    return format_byte_length(self.content_length)

  @property
  def url(self):

    if self.access == 'public' or \
      (current_user and self.access == 'authenticated_read'):
      return request.root_url[:-1] + url_for(
        "storage.get_object", 
        id=str(self.id)
      )

    signed_params = crypto.policy_encoder.encode(
      action="get_object",
      resource=str(self.id),
      expires_in=self.uri_expiration
    )

    return request.root_url[:-1] + url_for(
      "storage.get_object", 
      id=str(self.id), 
      **signed_params
    )

  @classmethod
  def generate_presigned_post(cls, **conditions):

    policy = crypto.policy_encoder.encode(
      action="put_object",
      resource=cls.__name__,
      expires_in=cls.uri_expiration,
      conditions=conditions
    )

    url = request.root_url[:-1] + url_for(
      "storage.upload"
    )

    fields = conditions.copy()
    fields.update(policy)
    fields['model'] = cls.__name__

    exclude_fields = [
      "content_length_range",
      "content_type",
      "content_types"
    ]

    for key in exclude_fields:
      if key in fields:
        fields.pop(key)

    return {
      "url": url,
      "fields": fields
    }

  def __str__(self):
    return f"{self.file_name}{': ' + (self.description or '')}"
  
  @queryset_manager
  def secured_objects(cls, qs):
    if current_user:
      if current_user.role.is_admin:
        return qs
      return qs(
        Q(user=current_user) |
        Q(access__in=[
          'authenticated_read',
          'public'
        ])
      )
    else:
      return qs(access='public')
