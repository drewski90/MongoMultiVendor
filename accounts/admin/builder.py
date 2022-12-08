from flask_admin import Admin as Admin_App

class AdminBuilder:
  """
    Wraps flask admin and allows views to be registered before initialization
  """

  def add_view(self, view):
    self.views.append(view)

  def add_views(self, *args):
    for view in args:
      self.views.append(view)

  def __init__(self):
    self.views = []
    self.initialized = False

  def __call__(self, flask_app, **kwargs):
    self.app = Admin_App(flask_app, **kwargs)
    for view in self.views:
      self.app.add_view(view)
    self.initialized = True

