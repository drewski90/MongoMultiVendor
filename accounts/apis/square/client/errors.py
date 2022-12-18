def error_handler(api_response):
  if api_response.is_success():
    return api_response.body
  elif api_response.is_error():
    raise Exception(api_response.body)
