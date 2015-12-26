import os
import djcelery
from celery.schedules import crontab

BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = ')c#(=l$5n+6xc7irx%7u(0)^%h##tj2d=v*_5#62m=o&zc_g7p'

DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

RAVEN_CONFIG = {
    'dsn': os.getenv('SENTRYDSN') if os.getenv('SENTRYDSN') else '',
}



INSTALLED_APPS = (
    'raven.contrib.django.raven_compat',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'haystack',
    'djcelery',
    'django_inbound_email',
    'micro_admin',
    'pages',
    'books',
    'micro_blog',
    'employee',
    'sorl.thumbnail',
    'compressor',
    'search',
)

MIDDLEWARE_CLASSES = (
    'django.middleware.cache.UpdateCacheMiddleware',
    'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
    'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
    'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',
    'microsite.middleware.RequestSessionMiddleware',
    'django.middleware.cache.FetchFromCacheMiddleware'
)


HTML_MINIFY = True

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.static',
    'django.core.context_processors.request',
    'django.core.context_processors.media',
)


ROOT_URLCONF = 'microsite.urls'

WSGI_APPLICATION = 'microsite.wsgi.application'
AUTH_USER_MODEL = 'micro_admin.User'

djcelery.setup_loader()

BROKER_URL = 'redis://localhost:6379/0'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'microsite',
        'USER': 'postgres',
        'PASSWORD': 'root',
        'HOST': '127.0.0.1',
        'PORT': '5432',
    }
}


LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = False

LOGIN_URL = '/portal/'

STATIC_URL = '/static/'

STATICFILES_DIRS = (BASE_DIR + '/static',)

COMPRESS_ROOT = BASE_DIR + '/static/'
BLOG_IMAGES = BASE_DIR + '/static/blog/'
TEAM_IMAGES = BASE_DIR + '/static/team/'
CLIENT_IMAGES = BASE_DIR + '/static/client/'
TRAINER_IMAGES = BASE_DIR + '/static/trainer/'
COURSE_IMAGES = BASE_DIR + '/static/course/'
QACAT_IMAGES = BASE_DIR + '/static/qacategory/'

TEMPLATE_DIRS = (BASE_DIR + '/templates',)

MEDIA_ROOT = BASE_DIR
SITE_BLOG_URL = "/blog/"

TEMPLATE_LOADERS = (
        "django.template.loaders.filesystem.Loader",
        "django.template.loaders.app_directories.Loader",
)

COMPRESS_ENABLED = True

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # other finders..
    'compressor.finders.CompressorFinder',
)

CELERY_TIMEZONE = "Asia/Calcutta"

CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"


CELERYBEAT_SCHEDULE = {
    # Executes every day evening at 5:00 PM GMT +5.30
    'add-every-day-evening': {
        'task': 'micro_blog.tasks.daily_report',
        'schedule': crontab(hour=17, minute=00, day_of_week='mon,tue,wed,thu,fri,sat'),
    },
}

SG_USER = os.getenv('SGUSER') if os.getenv('SGUSER') else ''
SG_PWD = os.getenv('SGPWD') if os.getenv('SGPWD') else ''

GOOGLE_ANALYTICS_CODE = os.getenv('GOOGLE_ANALYTICS_CODE') if os.getenv('GOOGLE_ANALYTICS_CODE') else ''

'''
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
'''

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.raven_compat.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

# ELASTICSEARCH_DEFAULT_ANALYZER = 'synonym_analyzer'

SITE_URL = "https://micropyramid.com"

# the fully-qualified path to the provider's backend parser
INBOUND_EMAIL_PARSER = 'django_inbound_email.backends.sendgrid.SendGridRequestParser'

# if True (default=False) then log the contents of each inbound request
INBOUND_EMAIL_LOG_REQUESTS = True

# if True (default=True) then always return HTTP status of 200 (may be required by provider)
INBOUND_EMAIL_RESPONSE_200 = True

COMPRESS_ENABLED = True

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
)

COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': 'STATIC_URL',
}

COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter']
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']
COMPRESS_REBUILD_TIMEOUT = 5400

query_cache_type = 0


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

#Haystack settings for Elasticsearch
HAYSTACK_CONNECTIONS = {
    'default': {
        'ENGINE': 'haystack.backends.elasticsearch_backend.ElasticsearchSearchEngine',
        'URL': 'http://127.0.0.1:9200/',
        'INDEX_NAME': 'haystack_post',
        'TIMEOUT': 60,
    },
}
HAYSTACK_SIGNAL_PROCESSOR = 'haystack.signals.RealtimeSignalProcessor'
HAYSTACK_DEFAULT_OPERATOR = 'OR'
HAYSTACK_SEARCH_RESULTS_PER_PAGE = 10

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

CACHE_MIDDLEWARE_ALIAS = 'default' #The cache alias to use for storage.
CACHE_MIDDLEWARE_SECONDS = 180 #The number of seconds each page should be cached.
CACHE_MIDDLEWARE_KEY_PREFIX = 'microsite'
CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
CACHE_IGNORE_REGEXPS = (
    r'/admin.*',
)
