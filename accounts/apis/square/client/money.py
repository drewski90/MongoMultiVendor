from pydantic import constr, conint
from .utils import Model

class Money(Model):

  amount:conint()
  currency:constr(
    strip_whitespace=True,
    strict=True
    )=None