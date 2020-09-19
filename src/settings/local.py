from inventory.settings import *
from django.conf import settings
from django.urls import include, path


ALLOWED_HOSTS = ['*']
DEBUG = True


DATABASES = {
    'default': env.db('SQLITE_URL', default='sqlite:////db.sqlite3')
}



# Local Static_root
STATIC_ROOT 	= os.path.join(os.path.dirname(BASE_DIR), 'static')
MEDIA_ROOT 		= os.path.join(os.path.dirname(BASE_DIR), 'images')