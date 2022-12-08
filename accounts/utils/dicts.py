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

class_to_dict = lambda cls:{
    k:getattr(cls, k) \
      for k in dir(cls) \
        if not k.startswith('__')
  }