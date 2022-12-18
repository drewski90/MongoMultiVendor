from ..media import Media
from .currencies import CODES as CURRENCY_CODES
from ..users import User
from uuid import uuid4
from datetime import datetime
from ..sessions import current_org
from ..organizations import (
  Organization,
  OrganizationLocation
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
  FloatField,
  GenericEmbeddedDocumentField,
  DateTimeField,
  DictField,
  PULL,
  CASCADE,
  NULLIFY,
  DENY
)

class ItemCategory(Document):
  meta = {
    "collection": "account_catalog_categories",
    "indexes": [
      "organization"
    ]
  }
  image = ReferenceField(Media)
  name = StringField()
  organization = ReferenceField(
    Organization, 
    required=True
  )
  parent = ReferenceField(lambda:ItemCategory)


class Price(EmbeddedDocument):
  tax_included = BooleanField()
  currency = StringField(
    default = "USD",
    choices = CURRENCY_CODES,
    null=False
    )
  amount = IntField(
    required=True,
    null=False
  )

class SubscriptionPrice(Price):
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
  interval_count = IntField(
    default=1,
    required=True
  )

class ServicePricing(Price):
  service_duration = IntField(required=True)
  notes = StringField()
  no_show_fee = EmbeddedDocument(
    Price
  )

class Item(Document):
  meta = {
    "collection": "account_catalog_item",
    "indexes": [
      "organization",
      ("category", "tags")
    ]
  }
  organization = ReferenceField(
    Organization,
    reverse_delete_rule=CASCADE
  )
  name = StringField(max_length=100)
  description = StringField(max_length=1000)
  image = ReferenceField(Media, reverse_delete_rule=DENY)
  purchase_note = StringField(max_length=255)
  category = ReferenceField(
    ItemCategory,
    reverse_delete_rule=NULLIFY
  )
  status = StringField(
    default="draft",
    choices=(
      'published'
      'draft', 
      'hidden',
      'deleted'
    )
  )
  upsell_items = ListField(
    ReferenceField(lambda:Item),
    reverse_delete_rule=PULL
    )
  cross_sell_items = ListField(
    ReferenceField(lambda:Item),
    reverse_delete_rule=PULL
  )
  default_price = GenericEmbeddedDocumentField(
    choices=(
      Price, 
      SubscriptionPrice,
    )
  )
  allow_ratings = BooleanField(default=False)
  metadata = DictField()
  tags = ListField(StringField, default=[])
  created = DateTimeField(default=datetime.utcnow)
  updated = DateTimeField(defatul=datetime.utcnow)

class ItemInventory(EmbeddedDocument):
  location = ReferenceField(
    OrganizationLocation, 
    required=True
  )
  quantity = IntField(default=-1)
  stock_note = StringField(max_length=255)
  in_store_pickup = BooleanField(default=True)
  delivery = BooleanField(default=True)

class ShippingDetail(EmbeddedDocument):

  class ShippingDimensions(EmbeddedDocument):
    width = StringField(required=True)
    height = StringField(required=True)
    length = StringField(required=True)
    unit = StringField()

  class ShippingWeight(EmbeddedDocument):
    value = FloatField(required=True)
    unit = StringField(required=True)
  
  free_shipping = BooleanField(default=False)
  weight = EmbeddedDocumentField(
    ShippingWeight, 
    required=True
  )
  dimensions = EmbeddedDocumentField(
    ShippingDimensions,
    required=True
  ) 

class ItemRating(Document):
  meta = {
    "collection": "account_catalog_ratings",
    "indexes": ['item']
  }
  user = ReferenceField(
    User,
    required=True,
    reverse_delete_rule=NULLIFY
  )
  item = ReferenceField(
    Item,
    required=True,
    reverse_delete_rule=CASCADE
  )
  rating = IntField(max=5)
  comment = StringField()
  media = ListField(
    ReferenceField(Media),
    reverse_delete_rule=PULL
  )

class ItemVariation(Document):
  meta = {
    "collection": "account_catalog_variations"
  }

  item = ReferenceField(Item, reverse_delete_rule=CASCADE)
  sku = StringField(max_length=80)
  name = StringField(max_length=80)
  description = StringField()
  images = ListField(Media, default=[], reverse_delete_rule=PULL)
  attributes = DictField()
  pricing = GenericEmbeddedDocumentField(
    choices=(
      Price, 
      SubscriptionPrice,
    )
  )
  inventory = ListField(
    EmbeddedDocumentField(
      ItemInventory
    ),
    default=[]
  )
  shipping = EmbeddedDocumentField(
    ShippingDetail
  )