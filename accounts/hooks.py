
BEFORE = "0"
AFTER = "1"

ROUTES = {}

def trigger(hook_name, *args, **kwargs):
  if hook_name in ROUTES:
    for f in ROUTES[hook_name]:
      result =  f(*args, **kwargs)
      if result:
        return result

def hooks(hook_name):
  def decorator(func):
    def wrapper(*args, **kwargs):
      result = trigger(
        f"{hook_name}.{BEFORE}", 
        *args, 
        **kwargs
      )
      if result:
        return result
      output = func(*args, **kwargs) or result
      result = trigger(
        f"{hook_name}.{AFTER}", 
        *args,
        result=output,
        **kwargs
      )
      if result:
        return result
      return output
    return wrapper
  return decorator

def watch(hook_name, order=AFTER):
  route = f"{hook_name}.{order}"
  if route not in ROUTES:
    ROUTES[route] = []
  def decorator(func):
    ROUTES[route].append(func)
    def wrapper(*args, **kwargs):
      result = func(*args, **kwargs)
      return result
    return wrapper
  return decorator
