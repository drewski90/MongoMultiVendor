from .dicts import dot_notation_get, class_to_dict
from .strings import snake_to_pascal, pascal_to_snake, pascal_to_title, ensure_https
from .document import populate_document
from .functions import set_static_kwargs
from .address import get_google_address

__all__ = [
  "get_google_address",
  "set_static_kwargs",
  "dot_notation_get",
  "snake_to_pascal",
  "pascal_to_snake",
  "pascal_to_title",
  "class_to_dict",
  "populate_document",
  "ensure_https",

]