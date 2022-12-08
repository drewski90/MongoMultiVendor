from mongoengine import FileField
from flask import Response
from .utils import get_file_size
from .base import Media
from ..sessions import current_user


class GFSMedia(Media):

  content = FileField(required=True)

  @classmethod
  def upload_file(cls, file, access='private'):

    media = cls(
      file_name=file.filename,
      content_type=file.content_type,
      content_length= get_file_size(file),
      access=access,
    )
    if current_user != None:
      media.uploader = current_user.id
    media.content.put(
      file, 
      content_type=file.content_type
    )
    media.save()

    return media

  def serve_file(self):
    return Response(
      self.content.read(), 
      mimetype=self.content_type
    )