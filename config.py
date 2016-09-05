import os


UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = set(['csv'])
TOKEN_SECRET = os.environ.get('this is a key') or 'this is a key'