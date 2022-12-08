class Webhooks:

  instance_list = []

  def __init__(self, flask_app):
    self.set_flask_app(flask_app)
  
  @classmethod
  def set_flask_app(cls, app):
    cls.flask_app = app
    for webhook in cls.instance_list:
      webhook.install(app)

  @classmethod
  def register_webhook(cls, wb):
    if getattr(cls, "flask_app", None):
      wb.install(cls.flask_app)
    cls.instance_list.append(wb)