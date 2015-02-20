import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = ')c#(=l$5n+6xc7irx%7u(0)^%h##tj2d=v*_5#62m=o&zc_g7p'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []


INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'djcelery',
    'django_inbound_email',
    'micro_admin',
    'pages',
    'micro_blog',
    'micro_kb',
    'employee',
    'sorl.thumbnail',
    'haystack',
    'compressor',
    'cachalot',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
)


# HTML_MINIFY = True

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
)


ROOT_URLCONF = 'microsite.urls'

WSGI_APPLICATION = 'microsite.wsgi.application'
AUTH_USER_MODEL = 'micro_admin.User'

import djcelery
djcelery.setup_loader()

BROKER_URL = 'redis://localhost:6379/0'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'micro',
        'USER': 'root',
        'PASSWORD': 'root',
    }
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False


STATIC_URL = '/static/'

STATICFILES_DIRS = (BASE_DIR + '/static',)

COMPRESS_ROOT=BASE_DIR + '/static/'
BLOG_IMAGES = BASE_DIR + '/static/blog/'
TEAM_IMAGES = BASE_DIR + '/static/team/'
CLIENT_IMAGES = BASE_DIR + '/static/client/'
TRAINER_IMAGES = BASE_DIR + '/static/trainer/'
COURSE_IMAGES = BASE_DIR + '/static/course/'
QACAT_IMAGES = BASE_DIR + '/static/qacategory/'

TEMPLATE_DIRS = (BASE_DIR +'/templates',)

MEDIA_ROOT = BASE_DIR
SITE_BLOG_URL = "/blog/"

TEMPLATE_LOADERS = (
    ("django.template.loaders.cached.Loader", (
        "django.template.loaders.filesystem.Loader",
        "django.template.loaders.app_directories.Loader",
    )),
)
COMPRESS_ENABLED=True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

CELERY_TIMEZONE="Asia/Calcutta"

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
from celery.schedules import crontab
from datetime import timedelta

CELERYBEAT_SCHEDULE = {
    # Executes every day evening at 5:00 PM GMT +5.30
    'add-every-day-evening': {
        'task': 'micro_blog.tasks.daily_report',
        'schedule': crontab(hour=18, minute=30, day_of_week='mon,tue,wed,thu,fri,sat'),
    },
}

 

SG_USER = os.getenv('SGUSER')
SG_PWD =  os.getenv('SGPWD')

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        }
    },
    'loggers': {
        'django.request': {
            'handlers': ['mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
    }
}



ELASTICSEARCH_DEFAULT_ANALYZER = 'synonym_analyzer'

SITE_URL = "http://micropyramid.com"

# the fully-qualified path to the provider's backend parser
INBOUND_EMAIL_PARSER = 'django_inbound_email.backends.sendgrid.SendGridRequestParser'

# if True (default=False) then log the contents of each inbound request
INBOUND_EMAIL_LOG_REQUESTS = True

# if True (default=True) then always return HTTP status of 200 (may be required by provider)
INBOUND_EMAIL_RESPONSE_200 = True

COMPRESS_ENABLED = True
COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter','compressor.filters.cssmin.CSSMinFilter']
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']
COMPRESS_REBUILD_TIMEOUT=5400

query_cache_type=0

CACHALOT_ENABLED=True
CACHALOT_CACHE_RANDOM=True

if 'TRAVIS' in os.environ:
    DATABASES = {
        'default': {
            'ENGINE':   'django.db.backends.mysql',
            'NAME':     'test',
            'USER':     'root',
            'PASSWORD': '',
            'HOST':     'localhost',
            'PORT':     '',
        }
    }