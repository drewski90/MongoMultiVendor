from .utils import APIModel, APIWrapper, Model
from .error import request_wrapper
from pydantic import constr, conint, conlist
from time import time
from typing import List, ForwardRef
from uuid import uuid4
from .money import Money
from random import randint
from .patterns import (
  RFC_3339_PATTERN,
  DATE_PATTERN,
  LOCAL_TIME_PATTERN
)
from .enums import *


CatalogObject = ForwardRef('CatalogObject')
CatalogItem = ForwardRef('CatalogItem')

class CatalogQuery(Model):
  class CatalogQuerySortedAttribute(Model):
    attribute_name:constr(
      strip_whitespace=True,
      min_length=1,
      strict=True
      )
    initial_attribute_value:constr(
      strip_whitespace=True,
      strict=True
    )
    sort_order:SquareSortOrderEnum

  class ExactQuery(Model):
    attribute_name:constr(
      strip_whitespace=True,
      min_length=1,
      strict=True
    )
    attribute_value:constr(
      strip_whitespace=True,
      min_length=1
    )

  class SetQuery(Model):
    attribute_name:constr(
      strip_whitespace=True,
      min_length=1,
      strict=True
    )
    attribute_values:List[constr(
      strip_whitespace=True,
      min_length=1,
      strict=True
    )]

  class PrefixQuery(Model):
    attribute_name:constr(
      strip_whitespace=True,
      min_length=1,
      strict=True
    )
    attribute_prefix:constr(
      strip_whitespace=True,
      min_length=1,
      strict=True
    )

  class RangeQuery(Model):
    attribute_name:constr(
      strip_whitespace=True,
      strict=True,
      min_length=1
    )
    attribute_min_value:conint()=None
    attribute_max_value:conint()=None

  class TextQuery(Model):
    keywords:List[constr(
      strip_whitespace=True,
      min_length=3,
      strict=True
    )]

  class ItemsForTaxQuery(Model):
    tax_ids:List[constr(
      strip_whitespace=True,
      min_length=1,
      strict=True
      )]

  class ItemsForModifierListQuery(Model):
    modifier_list_ids:List[constr(min_length=1)]

  class ItemsForItemOptionsQuery(Model):
    item_option_ids:List[constr(min_length=1)]

  class ItemVariationsForItemOptionValuesQuery(Model):
    item_option_value_ids:List[constr(min_length=1)]

  sorted_attribute_query:CatalogQuerySortedAttribute=None
  exact_query:ExactQuery=None
  set_query:SetQuery=None
  prefix_query:PrefixQuery=None
  range_query:RangeQuery=None
  text_query:TextQuery=None
  items_for_tax_query:ItemsForTaxQuery=None
  items_for_modifier_list_query:ItemsForModifierListQuery=None
  items_for_item_options_query:ItemsForItemOptionsQuery=None
  item_variations_for_item_option_values_query:ItemVariationsForItemOptionValuesQuery=None

class CatalogItem(Model):

  class CatalogItemVariation(Model):

    class ItemVariationLocationOverrides(Model):
      location_id:constr(
        strip_whitespace=True
      )=None
      price_money:Money=None
      pricing_type:SquareCatalogPricingTypeEnum=None
      track_inventory:bool=None
      inventory_alert_type:SquareInventoryAlertEnum=None
      inventory_alert_threshold:conint()=None
      sold_out:bool=None
      sold_out_valid_until:constr(
        regex=RFC_3339_PATTERN,
        strip_whitespace=True
      )=None

    class CatalogItemOptionValueForVariation(Model):
      item_option_id:constr(
        strip_whitespace=True
      )=None
      item_option_value_id:constr(
        strip_whitespace=True
      )=None

    class CatalogStockConversion(Model):

      stockable_item_variation_id:constr(
        strip_whitespace=True,
        min_length=1
      )
      stockable_quantity:constr(
        strip_whitespace=True,
        min_length=1,
        max_length=16
      )
      nonstockable_quantity:constr(
        strip_whitespace=True,
        min_length=1,
        max_length=16
      )

    id:str=None
    type:SquareItemTypeEnum="ITEM_VARIATION"
    item_id:constr(
        strip_whitespace=True
      )=None
    name:constr(
      strip_whitespace=True,
      max_length=255
    )=None
    sku:constr(
      strip_whitespace=True
    )=None
    upc:constr(
      strip_whitespace=True,
      max_length=14, 
      min_length=12
    )=None
    ordinal:conint()=None
    pricing_type:SquareCatalogPricingTypeEnum=None
    price_money:Money=None
    location_overrides:List[ItemVariationLocationOverrides]=None
    track_inventory:bool=None
    inventory_alert_type:SquareInventoryAlertEnum=None
    inventory_alert_threshold:conint()=None
    user_data:constr(
      strip_whitespace=True,
      max_length=255
    )=None
    service_duration:conint()=None
    available_for_booking:bool=None
    item_option_values:List[CatalogItemOptionValueForVariation]=None
    measurement_unit_id:constr()=None
    sellable:bool=None
    stockable:bool=None
    image_ids:List[
      constr(
        strip_whitespace=True
      )
    ]=None
    team_member_ids:List[
      constr(
        strip_whitespace=True
      )
    ]=None
    stockable_conversion:CatalogStockConversion=None

  class CatalogItemOption(Model):

    item_option_id:str=None

  name:str=None
  description_html:constr(
    strip_whitespace=True,
    max_length=4096
  )=None
  abbreviation:constr(
    strip_whitespace=True,
    max_length=24
  )=None
  label_color:constr(
    strip_whitespace=True
  )=None
  available_online:bool=None
  available_for_pickup:bool=None
  available_electronically:bool=None
  category_id:str=None
  tax_ids:List[str]=None
  modifier_list_info:List[str]=None
  variations:conlist(CatalogObject, min_items=1, unique_items=True)
  product_type:SquareCatalogItemProductTypeEnum
  skip_modifier_screen:bool=None
  item_options:List[CatalogItemOption]=None
  image_ids:List[str]=None
  sort_name:constr(
    strip_whitespace=True
  )=None
  description:constr(
    max_length=4096
  )=None
  description_html:constr(
    max_length=65535
  )
  description_plaintext:constr(
    max_length=65535
  )=None

class CatalogObject(APIModel):

  class CatalogItemModifierListInfo(Model):

    class CatalogModifierOverride(Model):
      modifier_id:constr(min_length=1)
      on_by_default:bool=None

    modifier_list_id:constr(min_length=1)
    modifier_overrides:CatalogModifierOverride=None
    min_selected_modifier:conint()=None
    max_selected_modifier:conint()=None
    enabled:bool=None

  class CatalogCustomAttributeValue(Model):

    name:constr(
      strip_whitespace=True,
      max_length=255
    )=None
    string_value:constr(
      strip_whitespace=True,
      max_length=255
    )=None
    custom_attribute_definition_id:constr(
      strip_whitespace=True,
      max_length=255
    )=None
    type:SquareCatalogCustomAttributeDefinitionTypeEnum=None

  class CatalogCategory(Model):
    name:constr(
      strip_whitespace=True,
      max_length=255
    )=None
    image_ids:List[constr(
      min_length=1,
      strip_whitespace=True
      )]=None

  class CatalogTax(Model):
    name:constr(
      strip_whitespace=True,
      max_length=255
    )=None
    calculation_phase:SquareTaxCalculationPhaseEnum=None
    inclusion_type:SquareTaxInclusionTypeEnum=None
    percentage:str=None
    applies_to_custom_amounts:bool=None
    enabled:bool=None

  class CatalogDiscount(Model):
    name:constr(
      strip_whitespace=True,
      max_length=255
    )=None
    discount_type:SquareCatalogDiscountTypeEnum=None
    percentage:constr(
      strip_whitespace=True
    )=None
    amount_money:Money=None
    pin_required:bool=None
    label_color:constr(
      strip_whitespace=True
    )=None
    modify_tax_basis:SquareCatalogDiscountModifyTaxBasisEnum=None
    maximum_amount_money:Money=None
  
  class CatalogModifierListItem(Model):
    name:constr(
      strip_whitespace=True
    )=None
    ordinal:int=None
    selection_type:SquareCatalogModifierListSelectionTypeEnum=None
    modifiers:List[CatalogItem]=None
    image_ids:List[str]=None

  class CatalogModifier(Model):
    name:constr(
      strip_whitespace=True
    )=None
    price_money:Money=None
    ordinal:int=None
    modifier_list_id:constr(
      strip_whitespace=True
    )=None
    image_id:constr(
      strip_whitespace=True
    )=None

  class CatalogTimePeriod(Model):
    event:str=None

  class CatalogProductSet(Model):
    name:constr(
      strip_whitespace=True,
      strict=True
    )=None
    product_ids_any:List[constr(
      strip_whitespace=True,
      min_length=1
    )]=None
    product_ids_all:List[constr(
      strip_whitespace=True,
      min_length=1
    )]=None
    quantity_exact:int=None
    quantity_min:int=None
    quantity_max:int=None
    all_products:bool=None

  class CatalogPricingRule(Model):
    name: constr(
      max_length=255, 
      strip_whitespace=True
    )=None
    time_period_ids:List[constr(
      strip_whitespace=True,
      )]=None
    discount_id:constr(
      strip_whitespace=True,
      max_length=255
    )=None
    match_products_id:constr(
      strip_whitespace=True
    )=None
    apply_products_id:constr(
      strip_whitespace=True,
    )=None
    exclude_products_id:constr(
      strip_whitespace=True
    )=None
    valid_from_date:constr(
      regex=DATE_PATTERN,
      strip_whitespace=True,
      strict=True
    )=None
    valid_from_local_time:constr(
      regex=LOCAL_TIME_PATTERN,
      strip_whitespace=True
    )=None
    valid_until_date:constr(
      regex=DATE_PATTERN,
      strip_whitespace=True
    )=None
    valid_until_local_time:constr(
      regex=LOCAL_TIME_PATTERN,
      strip_whitespace=True
    )=None
    exclude_strategy:SquareExcludeStrategyEnum=None
    minimum_order_subtotal_money:Money=None
    customer_group_ids_any:List[constr(
      strip_whitespace=True
    )]

  class CatalogImage(Model):
    name:constr(
      strip_whitespace=True,
    )=None
    url:constr(
      strip_whitespace=True
    )=None
    caption:constr(
      strip_whitespace=True
    )=None
    photo_studio_order_id:constr(
      strip_whitespace=True
    )=None

  class CatalogMeasurementUnit(Model):

    class MeasurementUnit(Model):

      class CustomUnit(Model):
        name:constr(
          strip_whitespace=True
        )
        abbreviation:constr(
          strip_whitespace=True
        )=None
  
      custom_unit:CustomUnit=None
      area_unit:SquareMeasurementUnitAreaEnum=None
      length_unit:SquareMeasurementUnitLengthEnum=None
      volume_unit:SquareMeasurementUnitVolumeEnum=None
      weight_unit:SquareMeasurementUnitWeightEnum=None
      generic_unit:SquareMeasurementUnitGenericEnum=None
      time_unit:SquareMeasurementUnitTimeEnum=None
      type:SquareMeasurementUnitTypeEnum=None

    measure_unit:MeasurementUnit
    percision:int

  class CatalogSubscriptionPlan(Model):

    class SubcriptionPhase(Model):

      uid:constr(strip_whitespace=True)=None
      cadence:SquareSubcriptionCadenceEnum
      periods:int=None
      recurring_price_money:Money
      ordinal:int=None

    name:constr(
      strip_whitespace=True,
      min_length=1
    )
    phases:List[SubcriptionPhase]

  class CatalogItemOption(Model):
    name:constr(strip_whitespace=True, min_length=1)=None
    display_name:constr(strip_whitespace=True, min_length=1)=None
    description:constr(strip_whitespace=True, min_length=1)=None
    show_colors:bool=None
    values:List[dict]=None

  class CatalogItemOptionValue(Model):
    item_option_id:constr(strip_whitespace=True)=None
    name:constr(strip_whitespace=True)=None
    description:constr(strip_whitespace=True)=None
    color:constr(strip_whitespace=True)=None
    ordinal:conint()=None

  class CatalogCustomAttributeDefinition(Model):

    class SourceApplication(Model):
      product:SquareProductEnum=None
      application_id:constr(strip_whitespace=True)=None
      name:str=None

    class CatalogCustomAttributeDefinitionStringConfig(Model):
      enforce_uniqueness:bool=None

    class CatalogCustomAttributeDefinitionNumberConfig(Model):
      precision:conint(le=5)=None
    
    class CatalogCustomAttributeDefinitionSelectionConfig(Model):
      
      class CatalogCustomAttributeDefinitionSelectionConfigCustomAttributeSelection(Model):

        uid:constr(strip_whitespace=True)=None
        name:constr(strip_whitespace=True)

      max_allowed_selections:conint(le=10)=None
      allowed_selections:conlist(
        CatalogCustomAttributeDefinitionSelectionConfigCustomAttributeSelection,
        max_items=100
      )=None
  
    type:SquareCatalogCustomAttributeDefinitionTypeEnum
    name:constr(strip_whitespace=True, max_length=255)
    description:constr(strip_whitespace=True, max_length=255)=None
    source_application:SourceApplication=None
    allowed_object_types:List[SquareItemTypeEnum]
    seller_visibility:SquareCatalogCustomAttributeDefinitionSellerVisibilityEnum=None
    app_visibility:SquareCatalogCustomAttributeDefinitionAppVisibilityEnum=None
    string_config:CatalogCustomAttributeDefinitionStringConfig=None
    number_config:CatalogCustomAttributeDefinitionNumberConfig=None
    selection_config:CatalogCustomAttributeDefinitionSelectionConfig=None
    custom_attribute_usage_count:int=None
    key:constr(
      regex=r'^[a-zA-Z0-9_-]*$', 
      min_length=1, 
      max_length=60
    )=None

  class CatalogQuickAmountsSettings(Model):

    class CatalogQuickAmount(Model):
      type:str
      amount:Money
      score:conint(le=100, ge=0)=None
      ordinal:int=None

    option:SquareCatalogQuickAmountsSettingsOptionEnum
    eligible_for_auto_amounts:bool=None
    amounts:List[CatalogQuickAmount]=None

  type:SquareItemTypeEnum=None
  id:str=None
  is_deleted:bool=None
  custom_attribute_value:dict=None
  catalog_v1_ids:List[str]=None
  present_at_all_locations:bool=None
  present_at_location_ids:List[str]=None
  absent_at_location_ids:List[str]=None
  item_data:CatalogItem=None
  category_data:CatalogCategory=None
  item_variation_data:CatalogItem.CatalogItemVariation=None
  tax_data:CatalogTax=None
  discount_data:CatalogDiscount=None
  modifier_list_data:List[CatalogModifierListItem]=None
  modifier_data:CatalogModifier=None
  time_period_data:CatalogTimePeriod=None
  product_set_data:CatalogProductSet=None
  pricing_rule_data:CatalogPricingRule=None
  image_data:CatalogImage=None
  measurement_unit_data:CatalogMeasurementUnit=None
  subscription_unit_data:CatalogSubscriptionPlan=None
  item_option_data:CatalogItemOption=None
  item_option_value_data:CatalogItemOptionValue=None
  custom_attribute_definition_data:CatalogCustomAttributeDefinition=None
  quick_amounts_settings_data:CatalogQuickAmountsSettings=None
  created_at:constr(
    strip_whitespace=True, 
    regex=RFC_3339_PATTERN
    )=None
  updated_at:constr(
    strip_whitespace=True, 
    regex=RFC_3339_PATTERN
    )=None
  version:conint()=None

  def dict(self, **kwargs):
    # stupid hack to get rid of version error
    if not self.version:
      self.version = int(time())
    return super(self.__class__, self).dict(**kwargs)

  def save(self, idempotency_key=None):
    if not self.id:
      self.id = "#" + str(uuid4())
    obj = self.dict(exclude_unset=True, exclude_none=True)
    body = request_wrapper(
      self.api.upsert_catalog_object,
      body={
        "idempotency_key": idempotency_key,
        "object": obj
      }
    )
    self.refresh(**body['catalog_object'])
    return self

  def update(self, idempotency_key=None):
    return self.save(idempotency_key)

  def delete(self):
    body = request_wrapper(
      self.api.delete_catalog_object,
      object_id=self.id
    )
    self.refresh(**body)
    return self

class CatalogObjectBatch(Model):
  objects:List[CatalogObject]

class Catalog(APIWrapper):
  api_name = "catalog"

  def create(
    self,
    type:SquareItemTypeEnum,
    is_deleted:bool=None,
    custom_attribute_value:dict=None,
    catalog_v1_ids:List[str]=None,
    present_at_all_locations:bool=None,
    present_at_location_ids:List[str]=None,
    absent_at_location_ids:List[str]=None,
    item_data:CatalogItem=None,
    category_data:CatalogObject.CatalogCategory=None,
    item_variation_data:CatalogItem.CatalogItemVariation=None,
    tax_data:CatalogObject.CatalogDiscount=None,
    modifier_list_data:List[CatalogObject.CatalogModifierListItem]=None,
    modifier_data:CatalogObject.CatalogModifier=None,
    time_period_data:CatalogObject.CatalogTimePeriod=None,
    product_set_data:CatalogObject.CatalogProductSet=None,
    pricing_rule_data:CatalogObject.CatalogPricingRule=None,
    image_data:CatalogObject.CatalogImage=None,
    measurement_unit_data:CatalogObject.CatalogMeasurementUnit=None,
    subscription_unit_data:CatalogObject.CatalogSubscriptionPlan=None,
    item_option_data:CatalogObject.CatalogItemOption=None,
    item_option_value_data:CatalogObject.CatalogItemOptionValue=None,
    custom_attribute_definition_data:CatalogObject.CatalogCustomAttributeDefinition=None,
    quick_amounts_settings_data:CatalogObject.CatalogQuickAmountsSettings=None,
    ) -> CatalogObject:
    obj = CatalogObject(
      api_wrapper=self,
      type=type,
      is_deleted=is_deleted,
      custom_attribute_value=custom_attribute_value,
      catalog_v1_ids=catalog_v1_ids,
      present_at_all_locations=present_at_all_locations,
      present_at_location_ids=present_at_location_ids,
      absent_at_location_ids=absent_at_location_ids,
      item_data=item_data,
      category_data=category_data,
      item_variation_data=item_variation_data,
      tax_data=tax_data,
      modifier_list_data=modifier_list_data,
      modifier_data=modifier_data,
      time_period_data=time_period_data,
      product_set_data=product_set_data,
      pricing_rule_data=pricing_rule_data,
      image_data=image_data,
      measurement_unit_data=measurement_unit_data,
      subscription_unit_data=subscription_unit_data,
      item_option_data=item_option_data,
      item_option_value_data=item_option_value_data,
      custom_attribute_definition_data=custom_attribute_definition_data,
      quick_amounts_settings_data=quick_amounts_settings_data,
    )
    obj.save()
    return obj

  def update(
    self,
    id:str,
    type:SquareItemTypeEnum,
    is_deleted:bool=None,
    custom_attribute_value:dict=None,
    catalog_v1_ids:List[str]=None,
    present_at_all_locations:bool=None,
    present_at_location_ids:List[str]=None,
    absent_at_location_ids:List[str]=None,
    item_data:CatalogItem=None,
    category_data:CatalogObject.CatalogCategory=None,
    item_variation_data:CatalogItem.CatalogItemVariation=None,
    tax_data:CatalogObject.CatalogDiscount=None,
    modifier_list_data:List[CatalogObject.CatalogModifierListItem]=None,
    modifier_data:CatalogObject.CatalogModifier=None,
    time_period_data:CatalogObject.CatalogTimePeriod=None,
    product_set_data:CatalogObject.CatalogProductSet=None,
    pricing_rule_data:CatalogObject.CatalogPricingRule=None,
    image_data:CatalogObject.CatalogImage=None,
    measurement_unit_data:CatalogObject.CatalogMeasurementUnit=None,
    subscription_unit_data:CatalogObject.CatalogSubscriptionPlan=None,
    item_option_data:CatalogObject.CatalogItemOption=None,
    item_option_value_data:CatalogObject.CatalogItemOptionValue=None,
    custom_attribute_definition_data:CatalogObject.CatalogCustomAttributeDefinition=None,
    quick_amounts_settings_data:CatalogObject.CatalogQuickAmountsSettings=None,
    ) -> CatalogObject:
    obj = CatalogObject(
      api_wrapper=self,
      id=id,
      type=type,
      is_deleted=is_deleted,
      custom_attribute_value=custom_attribute_value,
      catalog_v1_ids=catalog_v1_ids,
      present_at_all_locations=present_at_all_locations,
      present_at_location_ids=present_at_location_ids,
      absent_at_location_ids=absent_at_location_ids,
      item_data=item_data,
      category_data=category_data,
      item_variation_data=item_variation_data,
      tax_data=tax_data,
      modifier_list_data=modifier_list_data,
      modifier_data=modifier_data,
      time_period_data=time_period_data,
      product_set_data=product_set_data,
      pricing_rule_data=pricing_rule_data,
      image_data=image_data,
      measurement_unit_data=measurement_unit_data,
      subscription_unit_data=subscription_unit_data,
      item_option_data=item_option_data,
      item_option_value_data=item_option_value_data,
      custom_attribute_definition_data=custom_attribute_definition_data,
      quick_amounts_settings_data=quick_amounts_settings_data,
    )
    obj.update()
    return obj
  
  def items_search(
    self,
    text_filter:dict=None,
    category_ids:List[str]=None,
    stock_levels:List[str]=None,
    enabled_location_ids:List[str]=None,
    cursor:str=None,
    limit:int=None,
    sort_order:str=None,
    product_types:List[str]=None,
    custom_attribute_filters:List[dict]=None
  ):
    body = request_wrapper(
      self.api.search_catalog_items,
      body=dict(
        text_filter=text_filter,
        category_ids=category_ids,
        stock_levels=stock_levels,
        enabled_location_ids=enabled_location_ids,
        cursor=cursor,
        limit=limit,
        sort_order=sort_order,
        product_types=product_types,
        custom_attribute_filters=custom_attribute_filters
      )
    )
    if 'items' in body:
      body['items'] = [
        CatalogObject(
          api_wrapper=self,
          **obj
        ) for obj in body['items']
      ]
    return body

  def objects_search(
    self,
    cursor:str=None,
    object_types:List[str]=None,
    include_deleted_objects:bool=False,
    include_related_objects:bool=False,
    begin_time:str=None,
    query:dict=None,
    limit:int=None
    ) -> dict:
    body = request_wrapper(
      self.api.search_catalog_objects,
      body=dict(
        cursor=cursor,
        object_types=object_types,
        include_deleted_objects=include_deleted_objects,
        include_related_objects=include_related_objects,
        begin_time=begin_time,
        query=query,
        limit=limit
      )
    )
    if 'objects' in body:
      body['objects'] = [
        CatalogObject(
          api_wrapper=self,
          **obj
        ) for obj in body['objects']
      ]
    if 'related_objects' in body:
      body['related_objects'] = [
        CatalogObject(
          api_wrapper=self,
          **obj
        ) for obj in body['related_objects']
      ]
    return body

  def list(
    self, 
    cursor=None,
    types:List[SquareItemTypeEnum]=None,
    catalog_version=None
  ) -> dict:
    if types:
      types = [i.value for i in types]
    body = request_wrapper(
      self.api.list_catalog,
      cursor=cursor,
      types=types,
      catalog_version=catalog_version
    )
    if 'objects' in body:
      body['objects'] = [
        CatalogObject(
          api_wrapper=self,
          **obj
        ) for obj in body['objects']
      ]
    return body

  def delete(self, object_id:str):
    obj = CatalogObject(
      api_wrapper=self,
      id=object_id
    )
    obj.delete()
    return obj

  def catalog_info(self):
    return request_wrapper(
      self.api.catalog_info
    )

  def batch_delete(self, object_ids) -> dict:
    body = request_wrapper(
      self.api.batch_delete_catalog_objects,
      body=dict(object_ids=object_ids)
    )
    return body

  def batch_retrieve(self, object_ids:List[str]) -> dict:
    body = request_wrapper(
      self.api.batch_retrieve_catalog_objects,
      body=dict(object_ids=object_ids)
    )
    if 'objects' in body:
      body['objects'] = [
        CatalogObject(
          api_wrapper=self,
          **obj
        ) for obj in body['objects']
      ]
    if 'related_objects' in body:
      body['related_objects'] = [
        CatalogObject(
          api_wrapper=self,
          **obj
        ) for obj in body['related_objects']
      ]
    return body

  def batch_upsert(
    self, 
    idempotency_key:str,
    objects:List[CatalogObject]) -> dict:
    body = request_wrapper(
      self.api.batch_upsert_catalog_objects,
      body=dict(
        idempotency_key=idempotency_key,
        batches=dict(objects=objects)
      )
    )
    if 'objects' in body:
      body['objects'] = [
        CatalogObject(
          api_wrapper=self,
          **obj
        ) for obj in body['objects']
      ]
    return body
  
  def update_modifier_lists(
    self, 
    item_ids:List[str],
    modifier_lists_to_disable:List[str]=None,
    modifier_lists_to_enable:List[str]=None
    ):
    return request_wrapper(
      self.api.update_item_modifier_lists,
      body=dict(
        item_ids=item_ids,
        modifier_lists_to_disable=modifier_lists_to_disable,
        modifier_lists_to_enable=modifier_lists_to_enable
      )
    )

  def update_item_taxes(
    self,
    item_ids:List[str],
    taxes_to_disable:List[str]=None,
    taxes_to_enable:List[str]=None
  ):
    return request_wrapper(
      self.api.update_item_taxes,
      body=dict(
        item_ids=item_ids,
        taxes_to_disable=taxes_to_disable,
        taxes_to_enable=taxes_to_enable
      )
    )

  def delete(self, object_id:str):
    return request_wrapper(
      self.api.delete_catalog_object,
      object_id=object_id
    )

  def retrieve(
    self, 
    object_id:str,
    include_related_objects:bool=False,
    catalog_version:int=None
    ):
    body = request_wrapper(
      self.api.retrieve_catalog_object,
      object_id=object_id,
      include_related_objects=include_related_objects,
      catalog_version=catalog_version
    )
    if 'object' in body:
      body['object'] = CatalogObject(
        api_wrapper=self,
        **body['object']
      )
    return body   

  def update_catalog_image(
    self,
    image_id:str,
    idempotency_key=None,
    image_file=None,
    ):
    result = request_wrapper(
      self.api.update_catalog_image,
    )
    return
  

CatalogObject.update_forward_refs()
CatalogItem.update_forward_refs()