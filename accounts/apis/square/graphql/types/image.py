from graphene import (
  ObjectType, 
  String, 
  Boolean
)

class SquareImageType(ObjectType):

  id = String()
  name = String()
  url = String()
  all_locations = Boolean()
  is_deleted = Boolean()
  created = String()
  update = String()

  resolve_created = lambda r, c: r['created_at']
  resolve_updated = lambda r, c: r['updated_at']
  resolve_name = lambda r, c: r['image_data']['name']
  resolve_url = lambda r, c: r['image_data']['url']