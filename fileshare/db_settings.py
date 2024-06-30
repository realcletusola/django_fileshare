import os 
from dotenv import load_dotenv  

# load env variables
load_dotenv()


# Database
DATABASES = {
    'default': {
        'ENGINE': os.getenv('DATABASE_ENGINE'),
        'NAME': os.getenv('DATABASE_NAME'),
        'USER': os.getenv('DATABASE_USER'),
        'PASSWORD': os.getenv('DATABASE_PASSWORD'),
        'HOST': os.getenv('DATABASE_HOST'),
        'PORT': os.getenv('DATABASE_PORT'),
    }
}


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# custom user model 
AUTH_USER_MODEL = 'authentication.CustomUser'
