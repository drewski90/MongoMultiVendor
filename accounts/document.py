from mongoengine.document import Document
from .utils import pascal_to_snake

class FMADocumentMetaclass(type(Document)):

  def __new__(cls, name, bases, attrs):
    model = super().__new__(cls, name, bases, attrs)
    model.__snakename__ = pascal_to_snake(model.__name__)
    return model