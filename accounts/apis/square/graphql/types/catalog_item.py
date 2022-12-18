from graphene import (
  Field,
  ObjectType,
  String,
  Int,
  ID,
  Boolean,
  List
)
from .image import SquareImageType
from .category import SquareCategoryType

class SquareNoShowFeeType(ObjectType):
  price = Int()
  currency = String()
  resolve_price = lambda r,c:r['amount']

class SquareVariationType(ObjectType):
  id = ID()
  created = String()
  updated = String()
  version = Int()
  deleted = Boolean()
  present_at_all_locations = Boolean()
  name = String()
  ordinal = String()
  pricing_type = String()
  price = Int()
  currency = String()
  service_duration = Int()
  bookable = Boolean()
  sellable = Boolean()
  stockable = Boolean()
  no_show_fee = Field(SquareNoShowFeeType)
  team_member_ids = List(ID)

  resolve_created = lambda r,c:r['created_at']
  resolve_updated = lambda r,c:r['updated_at']
  resolve_version = lambda r,c:r['version']
  resolve_deleted = lambda r,c:r['is_deleted']
  resolve_present_at_all_locations = lambda r,c:r['present_at_all_locations']
  resolve_id = lambda r,c:r['id']
  resolve_name = lambda r,c:r['item_variation_data']['name']
  resolve_ordinal = lambda r,c:r['item_variation_data']['ordinal']
  resolve_pricing_type = lambda r,c:r['item_variation_data']['pricing_type']
  resolve_price = lambda r,c:r['item_variation_data'].get('price_money', {}).get('amount')
  resolve_currency = lambda r,c:r['item_variation_data'].get('price_money', {}).get('currency')
  resolve_service_duration = lambda r,c:r['item_variation_data']['service_duration'] / 1000
  resolve_bookable = lambda r,c:r['item_variation_data']['available_for_booking']
  resolve_sellable = lambda r,c:r['item_variation_data']['sellable']
  resolve_stockable = lambda r,c:r['item_variation_data']['stockable']
  resolve_no_show_fee = lambda r,c:r['item_variation_data'].get('no_show_fee')
  resolve_team_member_ids = lambda r,c:r['item_variation_data'].get('team_member_ids')

class SquareItemType(ObjectType):

  id = ID()
  category = ID()
  product_type = String()
  present_at_all_locations = Boolean()
  name = String()
  description = String()
  description_html = String()
  deleted = Boolean()
  taxable = Boolean()
  visibility = String()
  images = List(SquareImageType)
  category = Field(SquareCategoryType)
  bookable = String()
  variations = List(SquareVariationType)
  skip_modifier_screen = Boolean()
  product_type = String()
  created = String()
  updated = String()

  resolve_created = lambda r,c:r['created_at']
  resolve_updated = lambda r,c:r['updated_at']
  resolve_version = lambda r,c:r['version']
  resolve_name = lambda r,c:r['item_data']['name']
  resolve_description = lambda r,c:r['item_data']['description']
  resolve_description_html = lambda r,c:r['item_data']['description_html']
  resolve_taxable = lambda r,c:r['item_data']['is_taxable']
  resolve_deleted = lambda r,c:r['item_data']['is_deleted']
  resolve_category = lambda r,c:r['category']
  resolve_skip_modifier_screen = lambda r,c:r['item_data']['skip_modifier_screen']
  resolve_product_type = lambda r,c:r['item_data']['product_type']
  resolve_images = lambda r,c:r['images']
  resolve_variations = lambda r,c:r['item_data']['variations']