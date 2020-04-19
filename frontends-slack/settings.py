import os

DEBUG = bool(os.environ.get('DEBUG', False))
SLACK_SIGNING_SECRET = os.environ['SLACK_SIGNING_SECRET']
SERVER_HOST = os.environ.get('SERVER_HOST', '0.0.0.0')
SERVER_PORT = os.environ.get('SERVER_PORT', 80)
