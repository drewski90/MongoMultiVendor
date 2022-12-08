from graphene.types.generic import GenericScalar
from graphene import (
  Interface,
  ObjectType,
  String,
  Boolean,
  List,
  ID,
  Field
)

class Category(Interface):
  id = ID()
  name = String()
  images = List(String)
  description = String()

  @classmethod
  def resolve_type(cls, instance, info):
    if "type" in instance and instance['type'] == "CATEGORY":
      return SquareCategoryType

class SquareCategoryType(ObjectType):
  class Meta:
    interfaces = (Category,)

class Product(Interface):
  id = ID()
  images = List(String)
  name = String()
  billing_schema = String()
  tax_behavior = String()
  description = String()
  active = Boolean()
  bookable = Boolean()
  # variations = List(ProductTierType)
  metadata = GenericScalar()
  deleted = Boolean()
  updated = String()
  created = String()

  @classmethod
  def resolve_type(cls, instance, info):
    if "type" in instance and instance['type'] == "CATEGORY":
      return SquareCategoryType
  
class SquareProduct(ObjectType):
  class Meta:
    interface = (Product,)
  
  def resolve_id(r, c):
    return r['id']

  def resolve_images(r, c):
    return  r[]

{
        "type": "ITEM",
        "id": "AUZXHHWNYDGXSP5DC6P4OUQX",
        "updated_at": "2022-12-03T11:17:02.364Z",
        "created_at": "2022-10-18T04:59:53.918Z",
        "version": 1670066222364,
        "is_deleted": false,
        "present_at_all_locations": true,
        "item_data": {
          "name": "Swedish Massage",
          "description": "Enjoy a Swedish Massage Relaxation Massage Light to Medium pressure $130 60min. Beautiful nice Calm setting with calming sounds of Relaxation. Hot towel provided to ease muscles.Choice of Aromatherapy and infused water or herbal tea",
          "is_taxable": true,
          "visibility": "PRIVATE",
          "category_id": "SG3TI46EX737IWVBCBEOCY2J",
          "variations": [
            {
              "type": "ITEM_VARIATION",
              "id": "YOLJ5SQ6XQ5OKK5K533YWWQD",
              "updated_at": "2022-12-03T11:17:02.364Z",
              "created_at": "2022-10-18T04:59:53.918Z",
              "version": 1670066222364,
              "is_deleted": false,
              "present_at_all_locations": true,
              "item_variation_data": {
                "item_id": "AUZXHHWNYDGXSP5DC6P4OUQX",
                "name": "Regular",
                "ordinal": 1,
                "pricing_type": "VARIABLE_PRICING",
                "service_duration": 3600000,
                "price_description": "$130",
                "available_for_booking": true,
                "no_show_fee": {
                  "amount": 3000,
                  "currency": "USD"
                },
                "sellable": true,
                "stockable": true,
                "team_member_ids": [
                  "TMSKmEjb_yJp84bA"
                ]
              }
            },
            {
              "type": "ITEM_VARIATION",
              "id": "4333R7HV7OCY2II7JIX3YV3E",
              "updated_at": "2022-12-03T11:17:02.364Z",
              "created_at": "2022-12-03T11:17:02.364Z",
              "version": 1670066222364,
              "is_deleted": false,
              "present_at_all_locations": true,
              "item_variation_data": {
                "item_id": "AUZXHHWNYDGXSP5DC6P4OUQX",
                "name": "90 Minute Session",
                "ordinal": 2,
                "pricing_type": "FIXED_PRICING",
                "price_money": {
                  "amount": 16000,
                  "currency": "USD"
                },
                "service_duration": 3600000,
                "available_for_booking": true,
                "sellable": true,
                "stockable": true,
                "team_member_ids": [
                  "TMSKmEjb_yJp84bA"
                ]
              }
            }
          ],
          "product_type": "APPOINTMENTS_SERVICE",
          "skip_modifier_screen": false,
          "ecom_visibility": "UNINDEXED",
          "image_ids": [
            "3TDBQPYOYTFVTKLJJKDN2UBR"
          ],
          "description_html": "<p>Enjoy a Swedish Massage Relaxation Massage Light to Medium pressure $130 60min. Beautiful nice Calm setting with calming sounds of Relaxation. Hot towel provided to ease muscles.Choice of Aromatherapy and infused water or herbal tea</p>",
          "description_plaintext": "Enjoy a Swedish Massage Relaxation Massage Light to Medium pressure $130 60min. Beautiful nice Calm setting with calming sounds of Relaxation. Hot towel provided to ease muscles.Choice of Aromatherapy and infused water or herbal tea"
        }
      },
