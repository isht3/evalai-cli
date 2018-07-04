# Store all the varibales here
import os

from os.path import expanduser


AUTH_TOKEN_FILE_NAME = 'token.json'

AUTH_TOKEN_DIR = "{}/.evalai/".format(expanduser('~'))

AUTH_TOKEN_PATH = os.path.join(AUTH_TOKEN_DIR, AUTH_TOKEN_FILE_NAME)

API_HOST_URL = os.environ.get("EVALAI_API_URL", 'https://evalapi.cloudcv.org')

EVALAI_ERROR_CODES = [400, 401, 406]
