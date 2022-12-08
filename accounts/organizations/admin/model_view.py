from flask_admin.contrib.mongoengine import ModelView
from flask import (
  redirect, 
  url_for, 
  request, 
  flash, 
  render_template_string, 
  current_app
)
from ...sessions import current_user, current_account
from datetime import datetime
from flask_admin import babel, helpers as h
import inspect

class FieldChangeError(Exception):
  pass

def get_field_default_value(model, field):
  descriptor = getattr(model.__class__, field, None)
  default_value = descriptor.default
  if callable(default_value):
    return default_value()
  return default_value

class AccountModelView(ModelView):

  field_level_update_permissions = {}

  form_excluded_columns = ['created', 'status']

  column_exclude_list = ("cls", '_cls', 'CLS', 'Cls')

  def get_permission(self, action_name):
    action = self.model_name + "." + action_name
    admin_action = self.model_name + ".admin_" + action_name
    if not current_user:
      return False
    if current_user.has_permission(admin_action):
      return True
    if current_account:
      return current_account.has_permission(action)

  @property
  def model_name(self):
    return self.model.__snakename__

  @property
  def can_create(self):
    return self.get_permission('create')

  @property
  def can_update(self):
    return self.get_permission('update')

  @property
  def can_delete(self):
    return self.get_permission('delete')

  def is_action_allowed(self, name):
    return self.get_permission(name)

  def is_accessible(self):
    return self.get_permission('read')

  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('admin.index', next=request.url))

  def on_model_change(self, form, model, is_created):
    field_perms = self.field_level_update_permissions
    for field, permission in field_perms.items():

      if is_created and hasattr(model, field):

        if not current_account.has_permission(permission):
          default_value = get_field_default_value(model, field)
          value = getattr(model, field, None)
          if value != default_value:
            flash(
              f"Your do not have permission to set {field}. "
              f"Permisson required: ({permission})", 
              'error'
            )
          setattr(model, field, default_value)

      else:

        if field in self.field_change_permissions and \
           field in model._changed_fields and \
            not current_account.has_permission(permission):
          raise Exception(
            f"Your do not have permission to modify {field} value. Permisson required: ({permission})"
          )

  def get_query(self):
    if current_user.has_permission(self.model_name + ".admin_read"):
      return self.model.objects
    if current_account.has_permission(self.model_name + '.read'):
      return self.model.objects(
        organization=current_account.organization
      )

  def render_from_templates(self, file_name, **kwargs):
    # set kwargs
    kwargs['admin_view'] = self
    kwargs['admin_base_template'] = self.admin.base_template
    kwargs['_gettext'] = babel.gettext
    kwargs['_ngettext'] = babel.ngettext
    kwargs['h'] = h
    kwargs['get_url'] = self.get_url
    kwargs['config'] = current_app.config
    kwargs.update(self._template_args)
    # template loader
    current_path = "\\".join(inspect.getfile(self.__class__).split('\\')[:-1])
    file_path = f"{current_path}\\templates\\{file_name}"
    with open(file_path,'r', encoding = 'utf-8') as file:
      return render_template_string(file.read(), **kwargs)