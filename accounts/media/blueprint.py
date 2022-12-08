from flask_wtf.csrf import validate_csrf
from . import crypto
from ..sessions import current_user
from .base import Media
from json import dumps
from .utils import (
  get_file_size,
  get_media_model,
  validate_file_properties
)
from flask import (
  Blueprint, 
  request, 
  Response,
  url_for,
  redirect,
  flash,
  session
)

media_blueprint = Blueprint('storage', __name__, url_prefix="/media")

@media_blueprint.route('/objects/', methods=["POST"])
def upload():
  
  try:

    file = request.files.get('file')
    form = request.form
    assert file is not None, "File is not present"
    model = get_media_model(form.get('model'))
    assert model is not None, f"{form.get('model')} is not a registered model"
    content_length_range = model.content_length_range or [1, 16_000_000]
    content_length=int(request.headers.get('Content-Length') or 0)
    assert content_length <= 16_000_000, "File too large (16mb max)"
    validate_file_properties(
      content_type=file.content_type,
      content_types=getattr(model, 'content_types', []),
      content_length_range=content_length_range,
      content_length=content_length
    )
    if 'policy'in form and 'signature' in form:

      crypto.policy_encoder.decode(
        "put_object",
        form['policy'],
        form['signature']
      )
      instance = model.upload_file(file)
      return Response(
        dumps(instance.to_mongo(), default=str),
        status=200,
        mimetype="application/json"
      )

    if 'csrf_token' in form:

      validate_csrf(form['csrf_token'])
      file = request.files.get('file')
      model = get_media_model(form.get('model'))
      instance = model.upload_file(file)
      flash(f'{instance.file_name} has been uploaded')
      return redirect(url_for(request.args.get('next')))

  except Exception as e:
    if request.args.get('next'):
      flash(str(e))
      return redirect(url_for(request.args.get('next')))
    return Response(str(e), status=401)

  return Response("Invalid request", status=401)


@media_blueprint.route('/objects/<id>/', methods=["GET"])
def get_object(id):

  media = Media.objects.filter(
      id=id
    ).first()

  try:

    assert media is not None, \
      "Requested object does not exist"

    if media.access == "public":
      return media.serve_file()


    elif media.access == "authenticated_read":
      assert current_user != None, \
        "Log in required"
      return media.serve_file()

    elif media.access == "private":

      assert all([
        'policy' in request.args,
        'signature' in request.args,
        current_user != None
      ]), "Access Denied"

      policy = crypto.policy_encoder.decode(
        'get_object',
        request.args['policy'],
        request.args['signature']
      )

      assert policy['resource'] == id, \
        "Policy resource does not match object id"

      return media.serve_file()
    
    else:
      raise Exception('file access type not supported')

  except Exception as e:
    return Response(str(e), status=500)