from .base import Media
from time import time
from ..webhooks import Webhook
from ..sessions import current_user
from datetime import timedelta, datetime
from json import dumps
from .base import file_access_options
from inspect import isclass
from .crypto import open_private_key_file
from datetime import datetime
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from botocore.signers import CloudFrontSigner
from ..document import FMADocumentMetaclass
from flask import (
  request,
  Response
)
from uuid import uuid4
from ..utils import (
  populate_document, 
  pascal_to_snake
)
from .utils import (
  validate_file_properties,
  get_file_size,
)
from botocore.exceptions import (
  ClientError, 
  ParamValidationError
)
from mongoengine import (
  StringField,
  IntField,
  DateTimeField
)



def cloudfront_signer(key_id, private_key_location):

  private_key = open_private_key_file(private_key_location)
  sign = lambda msg:private_key.sign(msg, padding.PKCS1v15(), hashes.SHA1())
  make_date = lambda ttl:datetime.utcnow() + timedelta(seconds=ttl)
  signer = CloudFrontSigner(key_id, sign)

  @property
  def make_url(self, *args, **kwargs):
    # generate cloudfront signed url
    expires_in = make_date(self.uri_expiration)
    url = signer.generate_presigned_url(
      self.domain + self.key, 
      date_less_than=expires_in
    )
    return url

  def cls_decorator(cls):
    assert isclass(cls) and (
      issubclass(cls, S3Object) or cls == S3Object
    ), f"{cls} is not subclassed from S3Object"
    # replaces serve_file method
    cls.url = make_url
    return cls

  return cls_decorator

class S3MediaMetaclass(FMADocumentMetaclass):

  def __new__(cls, name, bases, attrs):
    model = super().__new__(cls, name, bases, attrs)
    callback_name = pascal_to_snake(model.__name__) + "_upload"
    model.webhook = Webhook(callback_name, model.save_from_webhook)
    return model

class S3Object(Media, metaclass=S3MediaMetaclass):

  access_conversions = {
    "public": "public-read",
    "private": "private",
    'authenticated_read': 'authenticated-read',
  }

  client = None
  domain = None
  bucket = None
  object_prefix = None
  content_types = None
  content_length_range = [0, 5_000_000_000]
  object_expiration = None

  meta = {
    # 'queryset_class': S3Queryset,
    'indexes': [
        {
          'fields': ['expiration'], 
          'expireAfterSeconds': 1,
          'cls': False
        }
    ]
  }
  
  file_name = StringField(max_length=255, required=False)
  description = StringField(max_length=1000)
  content_type = StringField(max_length=255, null=False)
  content_length = IntField(min=0, required=True)
  access = StringField(choices=file_access_options, default='private')
  created = DateTimeField(default=datetime.utcnow, required=True)
  updated = DateTimeField(default=datetime.utcnow, required=True)
  last_accessed = DateTimeField(default=datetime.utcnow, required=True)
  # S3 Specific fields
  etag = StringField(max_length=255, required=False)
  key = StringField(max_length=150, required=True)
  acl = StringField(max_length=80, default="private", choices=list(access_conversions.values()), required=True)
  version_id = StringField(min_length=1, max_length=80, required=False)
  expiration = DateTimeField(null=True, required=False)

  def __init__(self, *args, **kwargs):
    if self.domain and self.domain[-1] != "/":
      self.domain += "/"
    if self.client is None:
      raise Exception(f"No 'client' attribute on {self.__class__.__name__}")
    super(self.__class__, self).__init__(*args, **kwargs)

  @property
  def s3_object_params(self):
    params = {
      "Bucket": self.bucket,
      "Key": self.key
    }
    if self.version_id:
      params["VersionId"] = self.version_id
    return params

  @property
  def url(self):
    if self.access != "public":
      params = self.s3_object_params
      url = self.client.generate_presigned_url(
        'get_object',
        Params=params,
        ExpiresIn=self.uri_expiration
      )
      return url
    if self.domain:
      return self.domain + self.key
    return f"https://{self.bucket}.s3.amazonaws.com/{self.key}"

  def delete(self, *args, **kwargs):
    "delete from s3 first"
    try:
      self.client.delete_object(**self.s3_object_params)
    except ClientError as ex:
      if ex.response['Error']['Code'] == "NoSuchKey":
        pass
    super(self.__class__, self).delete(*args, **kwargs)

  def clean(self):

    if self.version_id is not None and len(self.version_id) == 0:
      self.version_id = None
    
    self.acl = self.access_conversions[self.access]
  
    if self.pk:
      assert 'uploader' not in getattr(self,'_changed_fields',[]), \
        "Object 'uploader' cannot be changed"

  def move_object(self, data, allow_overwrite=False):

    bucket = self.bucket
    destination_key = data['Key']
    source_key = data['CopySource']['Key']
    source_version = data['CopySource'].get("Versionid")

    # determine if a object exists at copy destination

    try:
      destination_object = self.client.head_object(
        Bucket=bucket,
        Key=destination_key
      )
    except:
      destination_object = None

    # determine if source object will be overwritten

    will_replace_source_object = \
    source_version is None and \
      destination_key == source_key

    # determine if destination object will be overwritten

    will_replace_destination_object = \
      destination_object is not None and \
      "VersionId" not in destination_object

    # prevent object overwrite a existing object if allow overwrite is none

    if all([
      will_replace_destination_object,
      will_replace_source_object == False,
      allow_overwrite == False
    ]):
      raise Exception(
        f'{bucket}:{destination_key} '
        'already exists (overwrite disabled)'
      )

    # attempt copy

    try:

      response = self.client.copy_object(**data)

      if 'VersionId' in response:
        self.version_id = response['VersionId']
      else:
        self.version_id = None

      # delete source if needed
      if not will_replace_destination_object:
        self.client.delete_object(
          **data['CopySource']
        )

    except ClientError as ex:
      code = ex.response['Error']['Code']
      if code == "NoSuchBucket":
        raise Exception('Destination bucket does not exist')
      elif code == "NoSuchKey":
        self.delete()
        raise Exception('This object no longer exists')
      elif code == "NoSuchVersion":
        self.version_id = None
      elif code == "Access Denied":
        raise Exception('Move access denied')
      else:
        raise
    except ParamValidationError as ex:
      raise Exception("Invalid request parameters")

    if all([
      will_replace_source_object == False,
      self.version_id is None
    ]):
      replaced_object = self.__class__.objects.filter(
        bucket=bucket,
        key=destination_key,
        version_id=None
      ).first()
      if replaced_object:
        replaced_object.delete()

  def save(self, *args, **kwargs):

    self.clean()

    if self.id is not None:

      changes = self._changed_fields

      if any([
        'key' in changes,
        'file_name' in changes,
        'access' in changes,
        'expiration' in changes
      ]):

        original = self.__class__.objects.get(id=self.id)

        copy_source = original.s3_object_params

        data = {
          "ACL":self.acl,
          "Bucket":self.bucket,
          "ContentType":self.content_type,
          "CopySource":copy_source,
          "Key":self.key,
          "Metadata": {
            "file_name": self.file_name,
            "access": self.access
          },
          "MetadataDirective":'REPLACE',
          "TaggingDirective": 'COPY'
        }

        if self.expiration:
          data["Expires"] = self.expiration

        self.move_object(
          data,
          allow_overwrite=any([
            'file_name' in changes,
            'acl' in changes,
            'expiration' in changes
          ])
        )

    self.updated = int(time())

    super(self.__class__, self).save(*args, **kwargs)

  @classmethod
  def generate_presigned_post(
    cls,
    file_name,
    content_length,
    content_type,
    access="private",
    key=None,
    **kwargs
  ):
    validate_file_properties(
      content_type=content_type,
      content_types=cls.content_types,
      content_length=content_length,
      content_length_range=cls.content_length_range
    )

    if key is None:
      key = str(uuid4())
    if cls.object_prefix:
      key = cls.object_prefix + key

    fields = {}
    conditions = []
    query = {
      "Key": key,
      "Bucket": cls.bucket,
      "Conditions": conditions,
      "Fields": fields
    }
    # set acl
    acl = cls.access_conversions[access]
    assert acl in cls.access_conversions.values(), \
        f"{acl} is not a valid acl"
    fields['acl'] = acl
    conditions.append({"acl": acl})
    # set content type
    fields['Content-Type'] = content_type
    conditions.append({"Content-Type": content_type})

    conditions.append([
      "content-length-range", 
      cls.content_length_range[0], 
      cls.content_length_range[1]
    ])
    # set url expiration
    assert isinstance(cls.uri_expiration, int), \
      "Expires in should be a integer that represents the" \
      "number of seconds the policy should be valid for"
    query['ExpiresIn'] = cls.uri_expiration
    # set redirect
    url_params = {'uploader': str(current_user.id)}
    redirect_url = cls.webhook.url(**url_params)
    field_name = 'success_action_redirect'
    fields[field_name] = redirect_url
    conditions.append({field_name: redirect_url})
    # set metadata
    metadata = {k:str(v) for k, v in kwargs.items()}
    metadata['access'] = access
    metadata['file_name'] = file_name
    metadata['confirm_url'] = cls.webhook.url(
      key=key,
      bucket=cls.bucket,
      **url_params
    )
    for key, value in metadata.items():
      fields["x-amz-meta-" + key] = value
      conditions.append({"x-amz-meta-" + key: value})
    # set object expiration
    if cls.object_expiration:
      if isinstance(cls.object_expiration, timedelta):
        expiration = datetime.utcnow() + cls.object_expiration
      if isinstance(cls.object_expiration, int):
        expiration = datetime.utcnow() + timedelta(
          seconds=cls.object_expiration
        )
      assert isinstance(expiration, datetime), \
        "expiration is not a instance of datetime"
      expiration =  expiration.isoformat()
      field_name = 'Expires'
      fields[field_name] = expiration
      conditions.append({field_name: expiration})

    return cls.client.generate_presigned_post(**query)

  @classmethod
  def webhook_url(cls):
    return cls.webhook.url()

  @classmethod
  def upload_file(
    cls,
    file,
    access="private"
    ):

    file_name = file.filename
    content_type = file.content_type
    content_length = get_file_size(file)
    acl = cls.access_conversions[access]
    key = (cls.object_prefix or '') + str(uuid4())

    reference = {
      "Bucket":cls.bucket,
      "Key": (cls.object_prefix or '') + key
    }
    
    request = {
      "Body": file,
      "ContentType": content_type,
      "ContentLength": content_length,
      "ACL": acl,
      "Metadata": {
        'acl': acl,
        'file_name': file_name
      }
    }

    request.update(reference)

    if cls.object_expiration:
      request['Expires'] = datetime.utcnow() + timedelta(
          seconds=cls.object_expiration
        )
    try:
      response = cls.client.put_object(**request)
    except Exception as e:
      raise Exception(f'A error occurred while uploading {file_name}')

    obj = cls(
      uploader=current_user,
      file_name=file_name,
      content_type=content_type,
      content_length=content_length,
      access=access,
      etag=response['ETag'],
      key=key,
      acl=acl,
      version_id=response.get('VersionId'),
      expiration=request.get('Expires')
    )

    obj.save()

    return obj

  @classmethod
  def save_from_webhook(cls):
    try:
      obj_head = cls.client.head_object(
        Bucket=request.args['bucket'], 
        Key=request.args['key']
      )
      data = {
        "content_length": obj_head['ContentLength'],
        "content_type": obj_head['ContentType'],
        "version_id": obj_head.get('VersionId'),
        "key": request.args['key']
      }
      data['expiration'] = obj_head.get('Expires')
      data.update(obj_head['Metadata'])
      if 'confirm_url' in data:
        data.pop('confirm_url')
    except:
      return Response('Error occured', status=500)

    # check if the object is already in the database
    instance = cls.objects(
      key=request.args['key'],
      version_id=obj_head.get('VersionId')
    ).first()

    if not instance:
      instance = cls()
      populate_document(instance, data)
      instance.save()

    return Response(
      dumps(instance.to_mongo(), default=str), 
      status=200,
      mimetype="application/json"
    )
