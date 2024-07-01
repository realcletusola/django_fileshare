import os 
from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# ensure logs directories exist
authentication_log_dir = os.path.join(BASE_DIR, 'logs', 'authentication') # set log dir for authentication app
users_log_dir = os.path.join(BASE_DIR, 'logs', 'users') # set log dir for users app
# creates directory or do nothing if it already exist
os.makedirs(authentication_log_dir, exist_ok=True) 
os.makedirs(users_log_dir, exist_ok=True) 


# logging configuration 
LOGGING = {
	'version':1,
	'disable_existing_loggers': False,
	'formatters': {
		'verbose': {
			'format': '{levelname} {asctime} {module} {message}',
			'style': '{',
		},
		'simple': {
			'format': '{levelname} {message}',
			'style': '{',
		},
	},
	'handlers': {
		'console': {
			'level': 'DEBUG',
			'class': 'logging.StreamHandler',
			'formatter': 'simple'
		},
		'authentication_file_error': { # authentication app log settings
			'level': 'ERROR',
			'class': 'logging.FileHandler',
			'filename': os.path.join(authentication_log_dir, 'error_logs.log'),
			'formatter': 'verbose'
		},
		'users_file_error': { # users app log settings
			'level': 'ERROR',
			'class': 'logging.FileHandler',
			'filename': os.path.join(users_log_dir, 'error_logs.log'),
			'formatter': 'verbose'
		},

	},
	'loggers': {
		'django': {
			'handlers': ['console'],
			'level': 'DEBUG',
			'propergate': True,
		},
		'authentication': { # authentication app logging type
			'handlers': ['console', 'authentication_file_error'],
			'level': 'DEBUG',
			'propergate': True,
		},
		'users': { # users app logging type
			'handlers': ['console', 'users_file_error'],
			'level': 'DEBUG',
			'propergate': True,
		},
	},
}