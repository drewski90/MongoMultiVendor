from flask_admin import babel, helpers as h, BaseView
from flask_admin.contrib.mongoengine import ModelView
from flask import render_template_string, current_app
import inspect


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

BaseView.render_from_templates = render_from_templates
ModelView.render_from_templates = render_from_templates