from flask_admin import babel
from flask_admin import helpers as h
from flask import render_template_string, current_app
from flask_admin.contrib.mongoengine import ModelView
from flask import redirect, url_for
from ...sessions import current_user
from datetime import datetime
import inspect

class FieldChangeError(Exception):
  pass

def get_field_default_value(model, field):
  descriptor = getattr(model.__class__, field, None)
  default_value = descriptor.default
  if callable(default_value):
    return default_value()
  return default_value


class UserModelView(ModelView):

  column_exclude_list = ("cls", '_cls', 'CLS', 'Cls')
  
  def get_query(self):
    if hasattr(self.model, 'secured_objects'):
      return self.model.secured_objects()
    return self.model.objects

  @property
  def model_name(self):
    return self.model.__snakename__

  @property
  def can_create(self):
    action = f"{self.model_name}.create"
    return current_user.role.has_permission(action)

  @property
  def can_edit(self):
    action = f"{self.model_name}.update"
    return current_user.role.has_permission(action)

  @property
  def can_delete(self):
    action = f"{self.model_name}.delete"
    return current_user.role.has_permission(action)

  def is_action_allowed(self, name):
    action = f"{self.model_name}.{name}"
    return current_user.role.has_permission(action)

  def is_accessible(self):
    return current_user != None

  def inaccessible_callback(self, name, **kwargs):
    return redirect(url_for('admin.index'))

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
