from .model_view import UserModelView

class RoleView(UserModelView): 

  form_widget_args = {
    'created': {
        'readonly': True
    }
  }


class UserPermissionView(UserModelView):
    pass