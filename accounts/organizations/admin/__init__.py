from .model_view import AccountModelView
from flask_admin.actions import action
from flask_admin import expose
from flask import url_for, redirect, request, flash

class OrganizationView(AccountModelView):
  form_excluded_columns = ['logo']

class BusinessAddressView(AccountModelView):
  pass

class AccountView(AccountModelView):
  pass

class AccountGroupView(AccountModelView):
  pass

class AccountPermissionView(AccountModelView):
  pass

class AccountRoleView(AccountModelView):
  pass

  