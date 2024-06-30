""" this file contains rest_framework, corsheaders and simpleJwt config """

import os 
# from pathlib import Path
from datetime import timedelta 
from dotenv import load_dotenv

# load env variables
load_dotenv()

# django secret key 
SECRET_KEY  = os.getenv('DJANGO_SECRET_KEY')


# rest_framework authentication backend 
# this has the custom auth backend which allows users login with either username or email 
AUTHENTICATION_BACKENDS = [
    "authentication.utils.CustomAuthBackend", "django.contrib.auth.backends.ModelBackend",
]

# rest_framework auth and permissions 
REST_FRAMEWORK = {
	"DEFAULT_AUTHENTICATION_CLASSES": (
		"rest_framework_simplejwt.authentication.JWTAuthentication", # JWT authentication 
	)
}

# JWT configuration
JWT_AUTH = {
	"JWT_PAYLOAD_HANDLER": "authentication.utils.custom_jwt_payload_handler", # this handler includes the username of the user in the jwt payload
}

SIMPLE_JWT = {
	"ACCESS_TOKEN_LIFETIME": timedelta(days=int(os.getenv('ACCESS_TOKEN_LIFETIME'))),
	"REFRESH_TOKEN_LIFETIME": timedelta(days=int(os.getenv('REFRESH_TOKEN_LIFETIME'))),
	"ROTATE_REFRESH_TOKENS": True,
	"BLACKLIST_AFTER_ROTATION": True,
	"UPDATE_LAST_LOGIN": True,

	"ALGORITHM": os.getenv('JWT_ALGORITHM'),
	"SIGNING_KEY": SECRET_KEY,
    'VERIFYING_KEY': None,
    'AUDIENCE': None,
    'ISSUER': None,
    'JWK_URL': None,
    'LEEWAY': 0,

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',

    "SLIDING_TOKEN_REFRESH_EXP_CLAIM": "refresh_exp",
    "SLIDING_TOKEN_LIFETIME": timedelta(minutes=int(os.getenv('SLIDING_TOKEN_LIFETIME'))),
    "SLIDING_TOKEN_REFRESH_LIFETIME": timedelta(days=int(os.getenv('SLIDING_TOKEN_REFRESH_LIFETIME'))),

}


# corsheaders config 
CORS_ALLOW_ALL_ORIGIN = True  # allows http requests from any server 