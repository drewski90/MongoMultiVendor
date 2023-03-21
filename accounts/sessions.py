from flask import request
from werkzeug.local import LocalProxy

class Users:

  USER_LOADERS = []

  USER_ID_KEY = "user"

  def _load_user():
    if user := getattr(request, Users.USER_ID_KEY, None):
      return user
    for func in Users.USER_LOADERS:
      result = func()
      if result is not None:
        if result.status == 'active':
          setattr(request, Users.USER_ID_KEY, result)
          return result
        raise Exception('Your user account is not active')

def user_loader(func):
  """registers a user loader function"""
  if func not in Users.USER_LOADERS:
    Users.USER_LOADERS.insert(0, func)
  def wrapper(*args, **kwargs):
    return func(*args, **kwargs)
  return wrapper

current_user = LocalProxy(Users._load_user)

def user_loaded(func):
  def wrapper(*args, **kwargs):
    if current_user == None:
      raise Exception('You are not logged in')
    return func(*args, **kwargs)
  return wrapper

# accounts

class Accounts:

  ACCOUNT_LOADERS = []
  ORGANIZATION_LOADERS = []
  ACCOUNT_ID_KEY = 'account'
  ORGANIZATION_ID_KEY = "organization"

  def _load_account():
    """same as user loader but for accounts"""
    if account := getattr(request, Accounts.ACCOUNT_ID_KEY, None):
      return account
    for func in Accounts.ACCOUNT_LOADERS:
      result = func()
      if result:
        setattr(request, Accounts.ACCOUNT_ID_KEY, result)
        if result and result.status == 'active':
          result.user = current_user
          return result
        else:
          raise Exception("Your account is no longer active")

  def _load_organization():
    if org := getattr(request, Accounts.ORGANIZATION_ID_KEY, None):
      return org
    else:
      for func in Accounts.ORGANIZATION_LOADERS:
        result = func()
        if result:
          setattr(request, Accounts.ORGANIZATION_ID_KEY, result)
          if result and result.status == 'active':
            result.user = current_user
            return result
          else:
            raise Exception("Your account is no longer active")

def account_loaded(func):
  def wrapper(*args, **kwargs):
    assert current_account != None, \
      'You are not logged in'
    return func(*args, **kwargs)
  return wrapper

def account_loader(func):
  """registers a account loader function"""
  if func not in Accounts.ACCOUNT_LOADERS:
    Accounts.ACCOUNT_LOADERS.insert(0, func)
  def wrapper(*args, **kwargs):
    return func(*args, **kwargs)
  return wrapper

def organization_loader(func):
  """registers a organization loader function"""
  if func not in Accounts.ORGANIZATION_LOADERS:
    Accounts.ORGANIZATION_LOADERS.insert(0, func)
  def wrapper(*args, **kwargs):
    return func(*args, **kwargs)
  return wrapper

current_account = LocalProxy(Accounts._load_account)
current_org = LocalProxy(Accounts._load_organization)