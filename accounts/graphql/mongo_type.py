from .scalars import ObjectId
from graphene import ObjectType
from graphene import (
    Node, 
    String, 
    List, 
    ObjectType
)

class MongoNode(Node):

  class Meta:
    name = 'MongoNode'

  @staticmethod
  def to_global_id(type, id):
    return id

class MongoType(ObjectType):
  id = ObjectId()
  cls = String()

  class Meta:
    interfaces = (MongoNode, )

  def resolve_cls(root, ctx):
    return root.__class__.__snakename__