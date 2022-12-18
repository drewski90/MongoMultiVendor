from flask import Flask, send_from_directory
from flask_cors import CORS
from flask_wtf.csrf import CSRFProtect
from accounts import App
import stripe
from accounts.media import S3Object, cloudfront_signer
import boto3
from os import environ

# temporary hacky way of setting environmental variables
if "Stripe_API_KEY" not in environ:
  with open('.env') as f:
    for i in f.readlines():
      if len(i.strip()) > 0:
        key, val = i.split('=')
        environ[key.strip()] = val.strip()

stripe.api_key = environ['STRIPE_API_KEY']

app = Flask(__name__)
app.debug = True
app.secret_key = environ['SECRET_KEY']
app.SESSION_COOKIE_SECURE = True
csrf = CSRFProtect(app)
cors = CORS(
  app, 
  supports_credentials=True,
  origins= [
    "*",
    "http://localhost:8080", 
    'http://192.168.1.78:8080/', 
    'https://192.168.1.78:8080/',
    'https://205f-108-235-115-70.ngrok.io'
  ],
  methods= [
    'POST', 
    "OPTIONS"
  ],
  headers=['Content-Type', 'Access-Control-Allow-Origin'],
  expose_headers=["Access-Control-Allow-Origin"],
  )


@app.route('/static/<path:path>')
def static_files(path):
    return send_from_directory('static', path)


S3Object.client = boto3.client(
  's3', 
  region_name=environ['AWS_REGION'],
  aws_access_key_id=environ['AWS_ACCESS_KEY'], 
  aws_secret_access_key=environ['AWS_SECRET_KEY']
)

S3Object.bucket = environ['S3_MEDIA_BUCKET']
S3Object.content_types = ['audio', 'video']
S3Object.domain = environ['CLOUDFRONT_DISTRIBUTION_URI']
cloudfront_signer(
  environ['CLOUDFRONT_KEY_ID'],
  environ['CLOUDFRONT_KEY_PATH']
  )(S3Object)

db_config = {
  'db': environ['DB_NAME'], 
  'host': environ['DB_HOST']
}

app.config['SQUARE'] = {
  "mode": environ['SQUARE_MODE'],
  "application_id": environ['SQUARE_APPLICATION_ID'],
  "production": {
    "access_token": environ.get('SQUARE_PRODUCTION_ACCESS_TOKEN'),
    "application_secret": environ.get('SQUARE_PRODUCTION_SECRET')
  },
  "sandbox": {
    "access_token": environ.get('SQUARE_SANDBOX_ACCESS_TOKEN'),
    "application_secret": environ.get('SQUARE_SANDBOX_SECRET')
  }
}

app.config['GOOGLE_API_KEY'] = environ['GOOGLE_API_KEY']


if __name__ == '__main__':
  App(
    app,
    db=db_config,
    app_name="Admin Panel", 
    organizations=True
  )
  app.run()