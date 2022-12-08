from mongoengine.document import Document
from .hooks import hooks, trigger, ROUTES, BEFORE, AFTER
from .utils import pascal_to_snake

def set_attr_wrapper(func):
  def wrapper(self, name, value):
    is_field = name[0] != "_" and name in self.__class__._fields
    is_initialised = getattr(self, '_initialised',None)
    if is_field and is_initialised and getattr(self, name, None) != value:
      before_hook = f"{BEFORE}.{self.__snakename__}.set.{name}"
      if all([is_field, before_hook]):
        trigger(before_hook, self=self, name=self, value=value)
      func(self, name, value)
      after_hook = f"{AFTER}.{self.__snakename__}.set.{name}"
      if all([is_field, after_hook in ROUTES]):
        trigger(after_hook, self=self, name=self, value=value)
    func(self, name, value)
  return wrapper

class FMADocumentMetaclass(type(Document)):

  def __new__(cls, name, bases, attrs):
    model = super().__new__(cls, name, bases, attrs)
    model.__snakename__ = pascal_to_snake(model.__name__)
    model.__setattr__ = set_attr_wrapper(model.__setattr__)
    if getattr(model, 'save', None):
      model.save = hooks(f'{model.__snakename__}.save')(model.save)
    if getattr(model, 'delete', None):
      model.delete = hooks(f'{model.__snakename__}.delete')(model.delete)
    return model