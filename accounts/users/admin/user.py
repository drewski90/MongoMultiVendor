from .model_view import UserModelView
from wtforms import form
import inspect
from wtforms import validators, FileField
from flask_admin import (
  expose, 
  babel, 
  BaseView, 
  helpers as h
)
from flask import (
  render_template_string, 
  current_app,
  url_for
)

class UserAuthView(BaseView):

  @expose('/')
  def index(self):
    return self.render_from_templates(
      "login_form.html"
    )

  @expose('/login/')
  def login_view(self):
    link = '<p>Don\'t have an account? <a href="' + url_for('.register_view') + '">Click here to register.</a></p>'
    self._template_args['form'] = form
    self._template_args['link'] = link
    return self.render_from_string(
      "fkflr;efk;elrkfe;lrk",
      form=form
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

class UserView(UserModelView):

  form_excluded_columns = ['avatar']

  form_extra_fields = {
    'image': FileField('Avatar', [validators.regexp(r'^[^/\\]\.jpg$')])
  }

  field_change_permissions = {
    "role": "user.assign role",
  }

  column_sortable_list = (
    'first_name', 
    'last_name',
  )

  column_exclude_list = (
    'password',
    '_cls'
    )
    
  form_excluded_columns = (
    'created',
    'status'
  )

  form_columns = [
    'first_name', 
    'last_name', 
    'email', 
    "groups",
    "role"
    ]
  

class UserAddressView(UserModelView):
  pass

