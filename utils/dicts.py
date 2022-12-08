def dot_notation_get(obj, field):
  pos = obj
  for key in field.split("."):
    if isinstance(pos, dict) and key in pos:
      pos = pos[key]
    elif hasattr(pos, key) or key in pos:
      pos = getattr(pos, key, None)
    else:
      return None
  return pos

def find_value_and_replace(obj, find_function, replace_function):
  for key, val in obj.items():
    if find_function(obj, key, val):
      return replace_function(obj, key, val)
    elif isinstance(val, dict):
      obj[key] = find_value_and_replace(
        obj[key],
        find_function,
        replace_function
      )
    elif isinstance(val, list):
      obj[key] = [
        find_value_and_replace(
          item, 
          find_function, 
          replace_function
        ) for item in val
      ]
  return obj

def merge_dicts(obj_a, obj_b, allow_overwrites=False):
  for key, val in obj_b.items():
    if key in obj_a and \
       obj_a[key] != val and \
        allow_overwrites is False:
      raise Exception(f"Property clash at ({key})")
    obj_a[key] = val
  return obj_a

