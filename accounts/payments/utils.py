from ..sessions import current_org

def get_square():
  test = lambda item: item.processor == 'square'
  square = next(filter(test, current_org.payment_processors), None)
  if square:
    return square
  raise Exception(f"There is no square account configured for {current_org.name}")

def get_processor(name):
  if name == "square":
    return get_square()