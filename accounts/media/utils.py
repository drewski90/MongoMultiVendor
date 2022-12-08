from mongoengine.base.common import _document_registry
from re import Pattern
from os import SEEK_END, SEEK_SET

def get_media_model(model_name):
  is_model = lambda m: m.__name__ == model_name
  model = next(filter(
    is_model, 
    _document_registry.values()
  ), None)
  assert model is not None, \
    f"{model_name} is not a registered media model"
  return model

def format_byte_length(num):
  if num < 1000:
    return f"{num} B"
  if num < 1_000_000:
    val = num / 1000
    return f"{val:.0f} KB"
  if num < 1_000_000_000:
    val = num / 1_000_000
    return f"{val:.2f} MB"
  else:    
    val = num / 1_000_000_000
    return f"{val:.2f} GB"

def get_file_size(file):
  file_size = file.seek(0, SEEK_END)
  file.seek(0, SEEK_SET)
  return int(file_size)

def validate_content_type(content_type, content_types):
  for _type in content_types:
    if isinstance(_type, str):
      if _type.lower() in content_type:
        return True
    if isinstance(_type, Pattern):
      res = _type.search(content_type)
      if res:
        return True
  raise Exception(f'Content type ({content_type}) not allowed')

def validate_content_length(content_length, content_length_range=None):
  if content_length_range:
    assert content_length is not None, \
      "content length not provided"
    assert isinstance(content_length_range, (tuple, list)), \
      "content length must be a list with two values (min, max)"
    assert len(content_length_range) == 2, \
      f"content length must contain two values, recieved {str(len(content_length_range))}"
    assert (isinstance(content_length_range[0], int) and isinstance(content_length_range[1], int)), \
      f"content length should be a range of two numbers, got ({str(content_length_range)})"
    min_bytes, max_bytes = content_length_range
    assert min(min_bytes, max_bytes) == min_bytes, \
      f"content range is invalid ({str(min_bytes)} to {str(max_bytes)})"
    assert min_bytes <= int(content_length) <= max_bytes, \
      f"File does not meet size requirements " \
      f"min({format_byte_length(min_bytes)}) "\
      f"max({format_byte_length(max_bytes)}), " \
      f"got ({format_byte_length(content_length)})"

def validate_file_properties(
  content_length=None,
  content_length_range=None,
  content_type=None,
  content_types=None,
  ):
  if content_length_range:
    validate_content_length(
      content_length,
      content_length_range
    )
  if content_types:
    validate_content_type(
      content_type,
      content_types
    )