from json import loads

class SquareRequestError(Exception):

  def __init__(self, errors):
    self.errors = errors

  def __str__(self):
    print(self.errors)
    error_messages = []
    for error in self.errors:
      if 'field' in error:
        msg = f"{error['field']}: {error['detail']}"
      else:
        msg = error['detail']
      error_messages.append(msg)
    return "\n".join(error_messages)

def request_wrapper(request_function, **kwargs):
  try:
    response = request_function(**kwargs)
    if response.is_success():
      return response.body
    elif response.is_error():
      raise SquareRequestError(response.body['errors'])
  except Exception as e:
    if hasattr(e, 'response') and e.response is not None:
      payload = loads(e.response.text)
      raise SquareRequestError(payload['errors'])
    else:
      raise e
