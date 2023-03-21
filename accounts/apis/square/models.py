from .client import SquareDocumentMixin
from datetime import datetime
from ...organizations import Organization
from ...sessions import current_org
from mongoengine import (
  StringField,
  DateTimeField,
  BooleanField,
  Document,
  ReferenceField,
  CASCADE
)

class SquareOAuth(Document, SquareDocumentMixin):
  meta = {
    "collection": "account_oauth",
    'indexes': ['organization']
  }
  organization = ReferenceField(
    Organization,
    default=lambda:current_org.id,
    reverse_delete_rule=CASCADE,
    null=False
  )
  merchant_id = StringField(max_length=90)
  access_token = StringField(max_length=255)
  refresh_token = StringField(max_length=255)
  token_type = StringField(max_length=255)
  short_lived = BooleanField(max_length=255)
  expiration = DateTimeField()
  created = DateTimeField(default=datetime.utcnow)

