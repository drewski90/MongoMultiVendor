from graphene import (
  ID,
  ObjectType,
  Boolean,
  String,
  Int
)

class SquareCategoryType(ObjectType):
  id = ID()
  updated = String()
  created = String()
  version = String()
  is_deleted = Boolean()
  all_locations = Boolean()
  name = String()
  ordinal = Int()
  is_top_level = Boolean()
  
  resolve_name = lambda r,c: r['category_data']['name']
  resolve_ordinal = lambda r, c: r['category_data']['ordinal']
  resolve_is_top_level = lambda r, c: r['category_data']['is_top_level']
