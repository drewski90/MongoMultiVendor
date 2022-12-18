from .catalog_item import SquareItemType
from .category import SquareCategoryType
from .subscription import SquareSubcriptionPlanType
from .image import SquareImageType
from graphene import (
  ObjectType,
  List
)

def insert_nested_data(item, data):
  if 'item_data' in item:
    if 'image_ids' in item['item_data']:
      img_ids = item['item_data']['image_ids']
      item['images'] = [
        i for i in data if i['type'] == "IMAGE" and i['id'] in img_ids
      ]
    else:
      item['images'] = []
    if 'category_id' in item['item_data']:
      cat_id = item['item_data']['category_id']
      item['category'] = next(filter(lambda i: i['id'] == cat_id, data), None)
  print("item", item)
  return item

class SquareCatalogType(ObjectType):

  items = List(SquareItemType)
  plans = List(SquareSubcriptionPlanType)
  categories = List(SquareCategoryType)
  images = List(SquareImageType)

  resolve_items = lambda r,c:[insert_nested_data(i, r) for i in r if i['type'] == "ITEM"]
  resolve_plans = lambda r,c:[insert_nested_data(i, r) for i in r if i['type'] == "SUBSCRIPTION_PLAN"]
  resolve_categories = lambda r,c:[i for i in r if i['type'] == "CATEGORY"]
  resolve_images = lambda r,c:[i for i in r if i['type'] == "IMAGE"]