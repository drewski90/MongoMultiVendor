from re import sub

def snake_to_pascal(s):
  assert isinstance(s, str), "Expected string but recieved {s} (snake_to_pascal)"
  return s.replace("_", " ").title().replace(" ", "")

def pascal_to_snake(s):
  assert isinstance(s, str), "Expected string but recieved {s} (pascal_to_snake)"
  return '_'.join(
    sub('([A-Z][a-z]+)', r' \1',
    sub('([A-Z]+)', r' \1',
    s.replace('-', ' '))).split()).lower()

def pascal_to_title(s):
  assert isinstance(s, str), "Expected string but recieved {s} (pascal_to_title)"
  return ' '.join(
    sub('([A-Z][a-z]+)', r' \1',
    sub('([A-Z]+)', r' \1',
    s.replace('-', ' '))).split())

def ensure_https(uri):
  if not uri.startswith("https://"):
    split = uri.split('://')
    if len(split) == 1:
      uri = "https://" + uri
    elif len(split) <= 2:
      split[0] = "https"
      uri = "://".join(split)
  return uri