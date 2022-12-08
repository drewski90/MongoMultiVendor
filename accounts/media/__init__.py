from .admin import MediaView
from .base import Media
from .gridfs import GFSMedia
from .blueprint import media_blueprint
from ..admin import Admin
from . import graphql
from . import crypto
from .s3 import (
  S3Object, 
  cloudfront_signer
)

def install_media(flask_app, private_key=None):

  if private_key:
    crypto.policy_parser = crypto.PolicyEncoder(
      private_key = private_key
    )

  Admin.add_view(
    MediaView(
      Media,
      name="Media",
      category="Media"
    )
  )
  Admin.add_view(
    MediaView(
      S3Object,
      name="Amazon S3",
      category="Media"
    )
  )
  Admin.add_view(
    MediaView(
      GFSMedia,
      name="Grid Fs",
      category="Media"
    )
  )

  if csrf := flask_app.extensions.get('csrf'):
    flask_app.register_blueprint(
      csrf.exempt(media_blueprint)
    )
  else:
    flask_app.register_blueprint(media_blueprint)

__all__ = [
  "Media"
  "Media",
  "GFSMedia",
  "S3Object", 
  "cloudfront_signer", 
  "s3_signer"
]
