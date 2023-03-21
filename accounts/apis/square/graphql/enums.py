from ..client import enums
from enum import Enum, EnumMeta
from graphene import Enum as g_enum

ENUMS = type("SquareEnums", (object, ), {
  key: g_enum.from_enum(getattr(enums, key)) 
  for key in dir(enums)
  if isinstance(getattr(enums, key), EnumMeta)
})
