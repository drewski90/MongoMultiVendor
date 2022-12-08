def set_static_kwargs(func, **static_kwargs):
  static_kwargs = {
    k:v for k,v in static_kwargs.items() if v is not None
  }
  # enforces static kwarg values
  def wrapper(*args, **kwargs):
    kwargs.update(static_kwargs)
    return func(*args, **kwargs)
  return wrapper