from mongoengine import BinaryField, StringField
from bcrypt import hashpw, checkpw, gensalt
from ..graphql import mongofield_conversion
from graphene import String
from re import compile

class MilitaryTimeField(StringField):

  regex = compile("([01]\d|2[0-3]):?[0-5]\d")

  def validate(self, value):
    super(MilitaryTimeField, self).validate(value)
    assert self.__class__.regex.search(value) is not None, \
      f"{value} is not formatted in military time (24hr format)"

class PasswordField(BinaryField):

  def __set__(self, obj, value):
    if isinstance(value, str):
      value = hashpw(
        value.encode('utf-8'), 
        gensalt()
      )
    return super(PasswordField, self).__set__(obj, value)

class PhoneNumberField(StringField):

  regex = compile("\+(9[976]\d|8[987530]\d|6[987]\d|5[90]\d|42\d|3[875]\d|2[98654321]\d|9[8543210]|8[6421]|6[6543210]|5[87654321]|4[987654310]|3[9643210]|2[70]|7|1)\d{1,14}$")
  
  def validate(self, value):
    super(PhoneNumberField, self).validate(value)
    assert self.__class__.regex.search(value) is not None, \
      "phone numbers require international code and + prefix"


@mongofield_conversion(PasswordField)
def to_string(required, **kwargs):
  return String(required=required)
