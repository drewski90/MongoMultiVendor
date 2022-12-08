from ..media import Media
from ..users import User
from uuid import uuid4
from datetime import datetime
from ..organizations import (
  Organization,
  Location
)
from mongoengine import (
  Document,
  ListField,
  ReferenceField,
  StringField,
  BooleanField,
  EmbeddedDocumentField,
  EmbeddedDocument,
  IntField,
  GenericEmbeddedDocumentField,
  DateTimeField
)

class ProductCategory(Document):
  image = ReferenceField(Media)
  name = StringField()
  organization = ReferenceField(
    Organization, 
    required=True
  )

class RecurringPrice(EmbeddedDocument):
  aggregate_useage = StringField(
    choices = (
      'sum',
      'last_ever'
      "last_during_period"
    )
  )
  interval = StringField(
    choices = (
      'month', 
      'year',
      'week',
      'day'
    ),
    requred=True,
    default='month'
  )
  interval = IntField(
    default=1,
    required=True
    )
  usage_type = StringField(
    choices=('metered', 'licensed'),
    required=True,
    default='licensed'
  )

class Price(EmbeddedDocument):
  id = StringField(default=lambda:str(uuid4))
  billing_schema = StringField(
    "tiered", "per_unit"
  )
  tax_behaviaor = StringField(
    choices=('exclusive', 'inclusive'),
    required=True
  )
  currency = StringField(default="USD")
  amount = IntField()
  recurring = EmbeddedDocumentField(
    RecurringPrice
  )
  type = StringField(
    choices=("one_time", 'recurring')
  )
  unit_amount = StringField()

class ProductDimensions(EmbeddedDocument):
  width = StringField()
  height = StringField()
  length = StringField()

class ExternalProduct(Document):
  payment_processor = StringField(
    choices=('square')
  )
  id = StringField()

class Product:
  external_product = EmbeddedDocument(
    ExternalProduct
  )
  organization = ReferenceField(Organization)
  available_for_pickup = BooleanField(default=False)
  classification = StringField(
    choices = (
      "physical",
      "service",
      "digital"
    ),
    default='service'
  )
  locations = ListField(
    ReferenceField(
      Location
    )
  )
  category = ReferenceField(ProductCategory)
  created = DateTimeField(
    default=lambda:datetime.utcnow()
  )

class ProductVariation(Document):
  product = ReferenceField(Product, required=True)
  attributes = ListField(EmbeddedDocumentField())
  updated = DateTimeField(default=datetime.utcnow)
  created = DateTimeField(default=datetime.utcnow)

class Order(Document):
  user = ReferenceField(User)
  organization = ReferenceField(
    Organization
  )
  line_items = ListField(
    GenericEmbeddedDocumentField(
      choices=[]
    ),
    required=True
    )