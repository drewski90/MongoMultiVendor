from ..users import UserModelView
from flask_admin import expose
from flask import Markup
from datetime import datetime
from ..sessions import current_user
from .base import Media

class MediaView(UserModelView):
  column_exclude_list = [
    'metadata',
    'content_length',
    'version',
    'etag',
    '_cls',
    'domain',
  ]
  column_list = (
    'id',
    'view',
    'file_name', 
    'content_type', 
    'size', 
    'type', 
    'access'
  )
  column_formatters = {
    'view': lambda v, ctx, model, name:Markup(f"""<a href="{model.url}">View</a>"""),
    'size': lambda v, ctx, model, name:model.file_size,
    "type": lambda v, ctx, model, name:model.__class__.__name__,
  }
  form_widget_args = {
    'version_id':{'disabled':True}
  }
  form_excluded_columns = (
    'content',
    'metadata',
    'content_length',
    'content_type',
    'created', 
    'updated',
    'version',
    'etag',
    'last_accessed',
    'acl',
    'uploader'
  )

  @property
  def can_create(self):
    return self.model != Media

  def is_accessible(self):
    if current_user:
      return current_user.has_permission(
        self.model.__snakename__ + '.read'
      )
    return False

  @expose('/new/', methods=('GET', 'POST'))
  def create_view(self):
    return self.render_from_templates(
      'upload_view.html', 
      return_url=self.get_url('.index_view')
    )