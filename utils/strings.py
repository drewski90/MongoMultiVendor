from re import compile, IGNORECASE, match

case_insensitive_strip_match = lambda string1, string2:string1.strip().lower() == string2.strip().lower()


def split_camelcase(string):
  res = []
  word = ""
  for char in string:
    if char.isupper() and len(word) > 0:
      res.append(word)
      word = ""
    word += char
  if len(word) > 0:
    res.append(word)
  return res

def camelcase_to_title(string):
  return " ".join(split_camelcase(string)).title()

def pascal_to_snake(string):
  return "_".join(split_camelcase(string)).lower()

def snake_to_pascal_to_camelcase(string):
  string = string.strip()
  flip_next = True
  new_str = ""
  for char in string:
    if char == "_":
      flip_next = True
    elif flip_next:
      flip_next = False
      new_str += char.upper()
    else:
      new_str += char.lower()
  return new_str