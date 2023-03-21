from graphene import (
  String,
  List,
  ID,
  Boolean,
  ObjectType,
  InputObjectType,
  Interface,
  Field,
  Int,
  Argument,
  Mutation
)
from .enums import ENUMS
from .money import SquareMoneyType, SquareMoneyInput
from graphene.types.generic import GenericScalar
from ..client.merchant import square_merchant

class SquareCatalogObject(Interface):

  id = ID()
  type = String()
  name = String()
  is_deleted = String()
  custom_attribute_value = GenericScalar()
  catalog_v1_ids=List(String)
  present_at_all_locations=Boolean()
  present_at_location_ids=List(String)
  absent_at_location_ids=List(String)
  created_at=String()
  updated_at=String()
  version=String()

  @classmethod
  def resolve_type(cls, instance, info):
    type = getattr(
      instance, 
      'type', 
      None
    )
    return OBJECT_TYPES[type]

class SquareCatalogItemType(ObjectType):

  resolve_type = lambda r,c: r.type

  class Meta:
    interfaces = (SquareCatalogObject,)

  class SquareCatalogItemDataType(ObjectType):

    class SquareCatalogItemVariation(ObjectType):

      class SquareItemVariationLocationOverridesType(ObjectType):
        
        location_id = String()
        price_money = Field(SquareMoneyType)
        pricing_type = String()
        track_inventory = Boolean()
        inventory_alert_type = Boolean()
        inventory_alert_threshold = Int()
        sold_out = Boolean()
        sold_out_valid_until = String()

      class SquareCatalogItemOptionValueForVariationType(ObjectType):
        
        item_option_id = String()
        item_option_value_id = String()

      class SquareCatalogStockConversionType(ObjectType):

        stockable_item_variation_id = String()
        stockable_quantity = String()
        nonstockable_quantity = String()
    
      id = String()
      type = String()
      item_id = String()
      name = String()
      sku = String()
      upc = String()
      ordinal = String()
      pricing_type = String()
      price_money = Field(SquareMoneyType)
      location_overrides = List(SquareItemVariationLocationOverridesType)
      track_inventory = Boolean()
      inventory_alert_type = String()
      inventory_alert_threshold = Int()
      user_data = String()
      service_duration = Int()
      available_for_booking = Boolean()
      item_option_values = List(SquareCatalogItemOptionValueForVariationType)
      measurement_unit_id = String()
      sellable = Boolean()
      stockable = Boolean()
      image_ids = List(ID)
      team_member_ids = List(ID)
      stockable_conversion = Field(SquareCatalogStockConversionType)
    
    class SquareCatalogItemOptionForItemType(ObjectType):
      
      item_option_id = String()

    name = String()
    description_html = String()
    abbreviation = String()
    label_color = String()
    available_online = Boolean()
    available_for_pickup = Boolean()
    available_electronically = Boolean()
    category_id = String()
    tax_ids = List(ID)
    modifier_list_info = List(String)
    variations = List(SquareCatalogObject)
    product_type = String()
    skip_modifier_screen = Boolean()
    item_options = List(SquareCatalogItemOptionForItemType)
    image_ids = List(ID)
    sort_name = String()
    description = String()
    description_html = String()
    description_plaintext = String()

  item_data = Field(SquareCatalogItemDataType, required=True)

class SquareCatalogCategoryType(ObjectType):

  resolve_type = lambda r,c: r.type

  class Meta:
    interfaces = (SquareCatalogObject, )

  class SquareCatalogCategoryDataType(ObjectType):
    name = String()
    image_ids = List(ID)

  category_data = Field(SquareCatalogCategoryDataType)

class SquareCatalogItemVariationType(ObjectType):

  resolve_type = lambda r,c: r.type

  class Meta:
    interfaces = (SquareCatalogObject, )

  class SquareCatalogItemVariationDataType(ObjectType):

    class SquareItemVariationLocationOverridesType(ObjectType):
      location_id = String()
      price_money = Field(SquareMoneyType)
      pricing_type = String()
      track_inventory = Boolean()
      inventory_alert_type = String()
      inventory_alert_threshold = Int()
      sold_out = Boolean()
      sold_out_valid_until = String()

    class SquareCatalogItemOptionValueForVariationType(ObjectType):
      item_option_id = String()
      item_option_value_id = String()

    class SquareCatalogStockConversionType(ObjectType):

      stockable_item_variation_id = String()
      stockable_quantity = String()
      nonstockable_quantity = String()

    id = ID()
    type = String()
    item_id = ID()
    name = String()
    sku = String()
    upc = String()
    ordinal = Int()
    pricing_type = String()
    price_money = Field(SquareMoneyType)
    location_overrides = List(SquareItemVariationLocationOverridesType)
    track_inventory = Boolean()
    inventory_alert_type = String()
    inventory_alert_threshold = String()
    user_data = String()
    service_duration = Int()
    available_for_booking = Boolean()
    item_option_values = List(SquareCatalogItemOptionValueForVariationType)
    measurement_unit_id = String()
    sellable = Boolean()
    stockable = Boolean()
    image_ids = List(ID)
    team_member_ids = List(ID)
    stockable_conversion = Field(SquareCatalogStockConversionType)

  item_variation_data = Field(SquareCatalogItemVariationDataType)

class SquareCatalogTaxType(ObjectType):

  resolve_type = lambda r,c: r.type

  class Meta:
    interfaces = (SquareCatalogObject, )

  class SquareCatalogTaxDataType(ObjectType):
    name = String()
    calculation_phase = String()
    inclusion_type = String()
    percentage = String()
    applies_to_custom_amounts = Boolean()
    enabled = Boolean()
  
  tax_data = Field(SquareCatalogTaxDataType)

class SquareCatalogDiscountType(ObjectType):

  resolve_type = lambda r,c: r.type

  class Meta:
    interfaces = (SquareCatalogObject,)

  class SquareCatalogDiscountDataType(ObjectType):
    name = String()
    discount_type = String()
    percentage = String()
    amount_money = Field(SquareMoneyType)
    pin_required = Boolean()
    label_color = Boolean()
    modify_tax_basis = Boolean()
    maximum_amount_money = Field(SquareMoneyType)

  discount_data = Field(SquareCatalogDiscountDataType)

class SquareCatalogModifierListItemType(ObjectType):

  resolve_type = lambda r,c: r.type

  class Meta:
    interfaces = (SquareCatalogObject,)
  
  class SquareCatalogModifierListItemDataType(ObjectType):
    name = String()
    ordinal = Int()
    selection_type = String()
    modifiers = List(SquareCatalogItemType)
    image_ids = List(ID)

  modifier_list_data = List(SquareCatalogModifierListItemDataType)

class SquareCatalogModifierType(ObjectType):
  
  class Meta:
    interfaces = (SquareCatalogObject,)

  class SquareCatalogModifierDataType(ObjectType):
    name = String()
    price_money = Field(SquareMoneyType)
    ordinal = Int()
    modifier_list_id = String()
    image_id = String()
  
  modifier_data = Field(SquareCatalogModifierDataType)

class SquareCatalogTimePeriodType(ObjectType):

  resolve_type = lambda r,c: r.type

  class Meta:
    interfaces = (SquareCatalogObject,)

  class SquareCatalogTimePeriodDataType(ObjectType):
    event = String()

  time_period_data = Field(SquareCatalogTimePeriodDataType)

class SquareCatalogProductSetType(ObjectType):

  resolve_type = lambda r,c: r.type

  class Meta:
    interfaces = (SquareCatalogObject,)

  class SquareCatalogProductSetDataType(ObjectType):
    name = String()
    product_ids_any = List(ID)
    product_ids_all = List(ID)
    quantity_exact = Int()
    quantity_min = Int()
    quantity_max = Int()
    all_products = Boolean()

  product_set_data = Field(SquareCatalogProductSetDataType)

class SquareCatalogPricingRuleType(ObjectType):

  resolve_type = lambda r,c: r.type

  class Meta:
    interfaces = (SquareCatalogObject,)

  class SquareCatalogPricingRuleDataType(ObjectType):
    name = String()
    time_period_ids = List(ID)
    discount_id = ID()
    match_products_id = ID()
    apply_products_id = ID()
    exclude_products_id = ID()
    valid_from_date = String()
    valid_from_local_time = String()
    valid_until_date = String()
    valid_until_local_time = String()
    exclude_strategy = String()
    minimum_order_subtotal_money = Field(SquareMoneyType)
    customer_group_ids_any = List(ID)
  
  pricing_rule_data = Field(SquareCatalogPricingRuleDataType)

class SquareCatalogImageType(ObjectType):
  
  resolve_type = lambda r,c: r.type

  class Meta:
    interfaces = (SquareCatalogObject,)

  class SquareCatalogImageDataType(ObjectType):
    name=String()
    url=String()
    caption=String()
    photo_studio_order_id=String()

  class Meta:
    interfaces = (SquareCatalogObject,)

  image_data = Field(SquareCatalogImageDataType)

class SquareCatalogMeasurementUnitType(ObjectType):
  
  resolve_type = lambda r,c: r.type

  class Meta:
    interfaces = (SquareCatalogObject,)

  class SquareCatalogMeasurementUnitDataType(ObjectType):

    class SquareMeasurementUnitType(ObjectType):

      class SquareCustomUnitType(ObjectType):
        name = String()
        abbreviation = String()
  
      custom_unit = Field(SquareCustomUnitType)
      area_unit = String()
      length_unit = String()
      volume_unit = String()
      weight_unit = String()
      generic_unit = String()
      time_unit = String()
      type = String()

    measure_unit = Field(SquareMeasurementUnitType)
    percision = Int()

  measurement_unit_data = Field(SquareCatalogMeasurementUnitDataType)

class SquareCatalogSubscriptionPlanType(ObjectType):
  
  resolve_type = lambda r,c: r.type

  class Meta:
    interfaces = (SquareCatalogObject,)

  class SquareCatalogSubscriptionPlanDataType(ObjectType):

    class SquareSubcriptionPhaseType(ObjectType):

      uid = String()
      cadence = String()
      periods = Int()
      recurring_price_money = Field(SquareMoneyType)
      ordinal = Int()

    name = String()
    phases = List(SquareSubcriptionPhaseType)
  
  subscription_unit_data = Field(SquareCatalogSubscriptionPlanDataType)

class SquareCatalogItemOptionType(ObjectType):

  resolve_type = lambda r,c: r.type

  class Meta:
    interfaces = (SquareCatalogObject,)

  class SquareCatalogItemOptionDataType(ObjectType):
    name = String()
    display_name = String()
    description = String()
    show_colors = Boolean()
    values = List(String)
  
  item_option_data = Field(SquareCatalogItemOptionDataType)

class SquareCatalogItemOptionValueType(ObjectType):
  resolve_type = lambda r,c: r.type
  class Meta:
    interfaces = (SquareCatalogObject,)

  class SquareCatalogItemOptionValueDataType(ObjectType):
    item_option_id = String()
    name = String()
    description = String()
    color = String()
    ordinal = Int()
  
  item_option_value_data = Field(SquareCatalogItemOptionValueDataType)

class SquareCatalogCustomAttributeDefinitionType(ObjectType):
  resolve_type = lambda r,c: r.type
  class Meta:
    interfaces = (SquareCatalogObject,)
  
  class SquareCatalogCustomAttributeDefinitionDataType(ObjectType):

    class SquareSourceApplicationType(ObjectType):
      product = String()
      application_id = String()
      name = String()

    class SquareCatalogCustomAttributeDefinitionStringConfigType(ObjectType):
      enforce_uniqueness = Boolean()

    class SquareCatalogCustomAttributeDefinitionNumberConfigType(ObjectType):
      precision = Int()
    
    class SquareCatalogCustomAttributeDefinitionSelectionConfigType(ObjectType):
      
      class SquareCatalogCustomAttributeDefinitionSelectionConfigCustomAttributeSelectionType(ObjectType):

        uid = String()
        name = String()

      max_allowed_selections = Int()
      allowed_selections = List(
        SquareCatalogCustomAttributeDefinitionSelectionConfigCustomAttributeSelectionType
      )

    type = String()
    name = String()
    description = String()
    source_application = Field(SquareSourceApplicationType)
    allowed_object_types = List(String)
    seller_visibility = String()
    app_visibility = String()
    string_config = Field(SquareCatalogCustomAttributeDefinitionStringConfigType)
    number_config = Field(SquareCatalogCustomAttributeDefinitionNumberConfigType)
    selection_config = Field(SquareCatalogCustomAttributeDefinitionSelectionConfigType)
    custom_attribute_usage_count = Int()
    key = String()
  
  custom_attribute_definition_data = Field(SquareCatalogCustomAttributeDefinitionDataType)

class SquareCatalogQuickAmountsSettingsType(ObjectType):
  resolve_type = lambda r,c: r.type
  class Meta:
    interfaces = (SquareCatalogObject,)

  class SquareCatalogQuickAmountsSettingsDataType(ObjectType):

      class SquareCatalogQuickAmountType(ObjectType):
        type = String()
        amount = Field(SquareMoneyType)
        score = Int()
        ordinal = Int()

      option = String()
      eligible_for_auto_amounts = Boolean()
      amounts = List(SquareCatalogQuickAmountType)
    
  quick_amounts_settings_data = Field(SquareCatalogQuickAmountsSettingsDataType)

OBJECT_TYPES = {
  "ITEM": SquareCatalogItemType,
  "CATEGORY": SquareCatalogCategoryType,
  "IMAGE": SquareCatalogImageType,
  "ITEM_VARIATION": SquareCatalogItemVariationType,
  "TAX": SquareCatalogTaxType,
  "DISCOUNT": SquareCatalogDiscountType,
  "MODIFIER_LIST": SquareCatalogModifierType,
  "MODIFIER": SquareCatalogModifierListItemType,
  "PRICING_RULE": SquareCatalogPricingRuleType,
  "TIME_PERIOD": SquareCatalogTimePeriodType,
  "MEASUREMENT_UNIT": SquareCatalogMeasurementUnitType,
  "ITEM_OPTION": SquareCatalogItemOptionType,
  "ITEM_OPTION_VAL": SquareCatalogItemOptionValueType,
  "CUSTOM_ATTRIBUTE_DEFINITION": SquareCatalogCustomAttributeDefinitionType,
  "QUICK_AMOUNTS_SETTINGS": SquareCatalogQuickAmountsSettingsType,
  "SUBSCRIPTION_PLAN": SquareCatalogSubscriptionPlanType
}

class SquareCatalogObjectInput(InputObjectType):

  class SquareCatalogCustomAttributeValueInput(InputObjectType):

    name = String()
    string_value = String()
    custom_attribute_definition = String()
    type = Argument(ENUMS.SquareCatalogCustomAttributeDefinitionTypeEnum)
    number_value = String()
    boolean_value = Boolean()
    selection_uid_values = List(String)
    key = String()

  class SquareCatalogItemInput(InputObjectType):

    class SquareCatalogItemModifierListInfoInput(InputObjectType):

      class SquareCatalogModifierOverrideInput(InputObjectType):
        
        modifier_id = String()
        on_by_default = Boolean()

      modifier_list_id = String()
      modifier_overrides = List(SquareCatalogModifierOverrideInput)
      min_selected_modifiers = Int()
      max_selected_modifiers = Int()
      enabled = Boolean()

    class SquareCatalogItemOptionForItemInput(InputObjectType):

      item_option_id = String(required=True)

    name = String()
    description = String()
    abbreviation = String()
    label_color = String()
    available_online = Boolean()
    available_for_pickup = Boolean()
    available_electronically = Boolean()
    category_id = ID()
    tax_ids = List(ID)
    modifier_list_info = SquareCatalogItemModifierListInfoInput()
    variations = List(lambda:SquareCatalogObjectInput)
    product_type = Argument(ENUMS.SquareCatalogItemProductTypeForFilterEnum)
    skip_modifier_screen = Boolean()
    item_options = List(SquareCatalogItemOptionForItemInput)
    image_ids = List(ID)
    sort_name = String()
    description_html = String()
    description_plaintext = String()

  class SquareCatalogCategoryInput(InputObjectType):

    name = String()
    image_ids = ID()

  class SquareCatalogItemVariationInput(InputObjectType):

    class SquareCatalogItemvariationLocationOverride(InputObjectType):
      
      location_id = ID()
      price_money = SquareMoneyInput()
      pricing_type = Argument(ENUMS.SquareCatalogPricingTypeEnum)
      track_inventory = Boolean()
      inventory_alert_type = Argument(ENUMS.SquareInventoryAlertEnum)
      inventory_alert_threshold = Int()
      sold_out = Boolean()
      sold_out_valid_until = String()

    class SquareCatalogItemOptionValueForItemVariationInput(InputObjectType):

      item_option_id = String()
      item_option_value_id = String()

    item_id = String()
    name = String()
    sku = String()
    upc = String()
    ordinal = Int()
    pricing_type = Argument(ENUMS.SquareCatalogPricingTypeEnum)
    price_money = SquareMoneyInput()
    location_overrides = List(SquareCatalogItemvariationLocationOverride)
    track_inventory = Boolean()
    inventory_alert_type = Argument(ENUMS.SquareInventoryAlertEnum)
    inventory_alert_threshold = Int()
    user_data = String()
    service_duration = Int()
    available_for_booking = Boolean()
    item_option_values = List(SquareCatalogItemOptionValueForItemVariationInput)
    measurement_unit_id = ID()
    sellable = Boolean()
    stockable = Boolean()
    stockable = Boolean()
    image_ids = List(ID)
    team_member_ids = List(ID)
    stockable_conversion = Argument(ENUMS.SquareCatalogStockConversion)

  class SquareCatalogTaxInput(InputObjectType):

    name = String()
    calculation_phase = Argument(ENUMS.SquareTaxCalculationPhaseEnum)
    inclusion_type = Argument(ENUMS.SquareTaxInclusionTypeEnum)
    percentage = String()
    applies_to_custom_amounts = Boolean()
    enabled = Boolean()

  class SquareCatalogDiscountInput(InputObjectType):

    name = String()
    discount_type = Argument(ENUMS.SquareCatalogDiscountTypeEnum)
    percentage = String()
    amount_money = SquareMoneyInput()
    pin_required = Boolean()
    label_color = String()
    modify_tax_basis = Argument(ENUMS.SquareCatalogDiscountModifyTaxBasisEnum)
    maximum_amount_money = SquareMoneyInput()

  class SquareCatalogModifierListInput(InputObjectType):
    
    name = String()
    ordinal = Int()
    selection_type = Argument(ENUMS.SquareCatalogModifierListSelectionTypeEnum)
    modifiers = List(lambda:SquareCatalogObjectInput)
    image_ids = List(ID)

  class SquareCatalogModifierInput(InputObjectType):
    
    name = String()
    price_money = SquareMoneyInput()
    ordinal = Int()
    modifier_list_id = String()
    images_id = List(String)

  class SquareCatalogTimePeriodInput(InputObjectType):
    
    event = String()

  class SquareCatalogProductSetInput(InputObjectType):
    
    name = String()
    product_ids_any = List(ID)
    product_ids_all = List(ID)
    quantity_exact = Int()
    quantity_min = Int()
    quantity_max = Int()
    all_products = Boolean()

  class SquareCatalogPricingRuleInput(InputObjectType):
    
    name = String()
    time_period_ids = List(ID)
    discount_id = ID()
    match_products_id = ID()
    apply_products_id = ID()
    exclude_products_id = ID()
    valid_from_date = String()
    valid_from_local_time = String()
    valid_until_date = String()
    valid_until_date_local_time = String()
    exclude_strategy = Argument(ENUMS.SquareExcludeStrategyEnum)
    minimum_order_subtotal_money = SquareMoneyInput()
    customer_group_ids_any = List(ID)

  class SquareCatalogImageInput(InputObjectType):
    
    name = String()
    url = String()
    caption = String()
    photo_studio_order_id = String()

  class SquareCatalogMeasurementUnitInput(InputObjectType):
    
    class SquareMeasurementUnit(InputObjectType):
      
      class SquareMeasurementUnitCustomInput(InputObjectType):
        
        name = String()
        abbreviation = String()
      
      custom_unit = SquareMeasurementUnitCustomInput()
      area_unit = Argument(ENUMS.SquareMeasurementUnitAreaEnum)
      length_unit = Argument(ENUMS.SquareMeasurementUnitLengthEnum)
      volume_unit = Argument(ENUMS.SquareMeasurementUnitVolumeEnum)
      weight_unit = Argument(ENUMS.SquareMeasurementUnitWeightEnum)
      generic_unit = Argument(ENUMS.SquareMeasurementUnitGenericEnum)
      time_unit = Argument(ENUMS.SquareMeasurementUnitTimeEnum)
      type = Argument(ENUMS.SquareMeasurementUnitTypeEnum)
    
    measurement_unit = String()
    percision = Int()
  
  class SquareCatalogSubscriptionPlanInput(InputObjectType):
    
    class SquareSubscriptionPhaseInput(InputObjectType):
      
      uid = ID()
      cadence = Argument(ENUMS.SquareSubcriptionCadenceEnum)
      periods = Int()
      recurring_price_money = SquareMoneyInput()
      ordinal = Int()
    
    name = String()
    phases = List(SquareSubscriptionPhaseInput)

  class SquareCatalogItemOptionInput(InputObjectType):
    
    name = String()
    display_name = String()
    description = String()
    show_colors = Boolean()
    values = List(lambda:SquareCatalogObjectInput)

  class SquareCatalogItemOptionValueInput(InputObjectType):
    
    item_option_id = ID()
    name = String()
    description = String()
    color = String()
    ordinal = Int()

  class SquareCatalogCustomAttributeDefinitionInput(InputObjectType):

    class SquareSourceApplicationInput(InputObjectType):
      
      product = Argument(ENUMS.SquareProductEnum)
      application_id = ID()
      name = String()

    class SquareCatalogCustomAttributeDefinitionStringConfigInput(InputObjectType):
      
      enforce_uniqueness = Boolean()

    class SquareCatalogCustomAttributeDefinitionNumberConfigInput(InputObjectType):
      
      precision = Int()

    class SquareCatalogCustomAttributeDefinitionSelectionConfigInput(InputObjectType):

      class SquareCatalogCustomAttributeDefinitionSelectionConfigCustomAttributeSelectionInput(InputObjectType):

        uid = ID()
        name = String()
      
      max_allowed_selections = Int()
      allowed_selections = List(SquareCatalogCustomAttributeDefinitionSelectionConfigCustomAttributeSelectionInput)

    type = Argument(ENUMS.SquareCatalogCustomAttributeDefinitionTypeEnum)
    name = String()
    description = String()
    source_application = SquareSourceApplicationInput()
    allowed_object_types = List(ENUMS.SquareItemTypeEnum)
    seller_visibility = Argument(ENUMS.SquareCatalogCustomAttributeDefinitionSellerVisibilityEnum)
    app_visibility = Argument(ENUMS.SquareCatalogCustomAttributeDefinitionAppVisibilityEnum)
    string_config = SquareCatalogCustomAttributeDefinitionStringConfigInput()
    number_config = SquareCatalogCustomAttributeDefinitionNumberConfigInput()
    selection_config = SquareCatalogCustomAttributeDefinitionSelectionConfigInput()
    custom_attribute_usage_count = Int()
    key = String()

  class SquareCatalogQuickAmountsSettingsInput(InputObjectType):

    class SquareQuickAmountInput(InputObjectType):

      type = String()
      amount = SquareMoneyInput()
      score = Int()
      ordinal = Int()

    option = Argument(ENUMS.SquareCatalogQuickAmountsSettingsOptionEnum)
    eligible_for_auto_amounts = Boolean()
    amounts = List(SquareQuickAmountInput)

  id = ID()
  type = Argument(ENUMS.SquareItemTypeEnum)
  version = Int()
  is_deleted = Boolean()
  custom_attribute_values = List(SquareCatalogCustomAttributeValueInput)
  catalog_v1_ids = List(ID)
  present_at_all_locations = List(ID)
  present_at_location_ids = List(ID)
  absent_at_location_ids = List(ID)
  item_data = SquareCatalogItemInput()
  category_data = SquareCatalogCategoryInput()
  tax_data = SquareCatalogTaxInput()
  discount_data = SquareCatalogDiscountInput()
  modifier_list_data = SquareCatalogModifierListInput()
  modifier_data = SquareCatalogModifierInput()
  time_period_data = SquareCatalogTimePeriodInput()
  product_set_data = SquareCatalogProductSetInput()
  product_rule_data = SquareCatalogPricingRuleInput()
  image_data = SquareCatalogImageInput()
  measurement_unit_data = SquareCatalogMeasurementUnitInput()
  subscription_plan_data = SquareCatalogSubscriptionPlanInput()
  item_option_data = SquareCatalogItemOptionInput()
  item_option_value_data = SquareCatalogItemOptionValueInput()
  custom_attribute_definition_data = SquareCatalogCustomAttributeDefinitionInput()
  quick_amounts_settings_data = SquareCatalogQuickAmountsSettingsInput()

class SquareCatalogObjectsResultsType(ObjectType):
  cursor = String()
  objects = List(SquareCatalogObject)
  related_objects = List(SquareCatalogObject)
  latest_time = String()

class SquareCatalogResultType(ObjectType):

  object = Field(SquareCatalogObject)
  related_objects = List(SquareCatalogObject)

class SquareCatalogItemsResultsType(ObjectType):
  cursor = String()
  items = List(SquareCatalogItemType)
  matched_variation_ids = List(ID)

class SquareCatalogObjectsFilterInput(InputObjectType):
  
  class SquareCatalogQueryInput(InputObjectType):
    
    class SquareCatalogQueryExactInput(InputObjectType):
      attribute_name = String()
      attribute_value = String()

    class SquareCatalogQuerySetInput(InputObjectType):
      attribute_name = String()
      attibute_values = List(String)

    class SquareCatalogPrefixInput(InputObjectType):
      attribute_name = String()
      attribute_prefix = String()

    class SquareCatalogQueryRangeInput(InputObjectType):
      attribute_name = String()
      attibute_min_value = Int()
      attribute_max_value = Int()

    class SquareCatalogQueryTextInput(InputObjectType):
      keywords = List(String)

    class SquareCatalogQueryItemsForTaxInput(InputObjectType):
      tax_ids = List(ID)

    class SquareCatalogQueryItemsForModifierListInput(InputObjectType):
      modifier_list_ids = List(ID)
    
    class SquareCatalogQueryItemsForItemOptionsInput(InputObjectType):
      item_option_ids = List(ID)

    class SquareCatalogQueryItemVariationsForItemOptionValues(InputObjectType):
      item_option_value_ids = List(ID)
    
    exact_query = SquareCatalogQueryExactInput()
    set_query = SquareCatalogQuerySetInput()
    prefix_query = SquareCatalogPrefixInput()
    range_query = SquareCatalogQueryRangeInput()
    text_query = SquareCatalogQueryTextInput()
    items_for_tax_query = SquareCatalogQueryItemsForTaxInput()
    items_for_modifier_list_query = SquareCatalogQueryItemsForModifierListInput()
    items_for_item_options_query = SquareCatalogQueryItemsForItemOptionsInput()
    item_variations_for_item_option_values_query = SquareCatalogQueryItemVariationsForItemOptionValues()
  
  object_types = List(ENUMS.SquareItemTypeEnum)
  include_deleted_objects = Boolean()
  include_related_objects = Boolean()
  begin_time = String()
  query = SquareCatalogQueryInput()

class SquareCatalogObjectsPaginationInput(InputObjectType):
  cursor = String()
  limit = int()

class SquareCatalogItemsFilterInput(InputObjectType):
  
  class SquareCatalogItemsCustomAttributeFilterInput(InputObjectType):

    class SquareNumberRangeInput(InputObjectType):
      min = Int()
      max = Int()

    custom_attribute_definition_id = String()
    key = String()
    string_filter = String()
    number_filter = SquareNumberRangeInput()
    selections_uids_filter = List(ID)
    bool_filter = Boolean()

  text_filter = String()
  category_ids = List(ID)
  stock_levels = Argument(ENUMS.SquareSearchCatalogItemsRequestStockLevelEnum)
  enabled_location_ids = List(ID)
  product_types = List(ENUMS.SquareCatalogItemProductTypeForFilterEnum)
  custom_attribute_filter = List(SquareCatalogItemsCustomAttributeFilterInput)

class SquareCatalogItemsPaginationInput(InputObjectType):
  cursor = String()
  limit = Int()
  sort_order = Argument(ENUMS.SquareSortOrderEnum)

class SquareCatalogInfoType(ObjectType):

  class SquareCatalogInfoLimitType(ObjectType):

    batch_upsert_max_objects_per_batch = Int()
    batch_upsert_max_total_objects = Int()
    batch_retrieve_max_object_ids = Int()
    search_max_page_limit = Int()
    batch_delete_max_object_ids = Int()
    update_item_taxes_max_item_ids = Int()
    update_item_taxes_max_taxes_to_enable = Int()
    update_item_taxes_max_taxes_to_disable = Int()
    update_item_modifier_lists_max_item_ids = Int()
    update_item_modifier_lists_max_modifier_lists_to_enable = Int()
    update_item_modifier_lists_max_modifier_lists_to_disable = Int()

  class StandardCatlogStandardUnitDescriptionGroupType(ObjectType):
  
    class SquareStandardUnitDescriptionType(ObjectType):

      unit = Field(SquareCatalogObjectInput.SquareCatalogMeasurementUnitInput.SquareMeasurementUnit)
      name = String()
      abbreviation = String()
  
    language_code = String()

  limits = Field(SquareCatalogInfoLimitType)
  standard_unit_description_group = Field(StandardCatlogStandardUnitDescriptionGroupType)

class SquareCatalogBatchUpsert(Mutation):

  objects = List(SquareCatalogObject)
  updated_at = String()
  id_mappings = List(String)

  class Arguments:
    idempotency_key = String(required=True)
    objects = List(SquareCatalogObjectInput)
  
  def mutate(root, ctx, **kwargs):
    api = square_merchant.catalog
    result = api.batch_upsert_catalog_objects(
      **kwargs
    )
    return SquareCatalogBatchUpsert(**result)

class SquareCatalogBatchDelete(Mutation):

  deleted_object_ids = List(ID)
  deleted_at = String()

  class Arguments:
    object_ids = List(ID)

  def mutate(root, ctx, object_ids):
    return SquareCatalogBatchDelete(
      **square_merchant.catalog.batch_delete(
        object_ids
      )
    )

class SquareCatalogUpdateItemModifierLists(Mutation):

  updated_at = String()
  
  class Arguments:

    item_ids = List(ID)
    modifier_lists_to_disable = List(ID)
    modifier_lists_to_enable = List(ID)

  def mutate(root, ctx, **kwargs):
    return SquareCatalogUpdateItemModifierLists(
      **square_merchant.catalog.update_modifier_lists(
        **kwargs
      )
    )

class SquareCatalogUpdateItemTaxes(Mutation):

  updated_at = String()

  class Arguments:

    item_ids = List(ID)
    taxes_to_disable = List(ID)
    taxes_to_enable = List(ID)

  def mutate(root, ctx, **kwargs):
    return SquareCatalogUpdateItemTaxes(
      **square_merchant.catalog.update_item_taxes(
        **kwargs
      )
    )


