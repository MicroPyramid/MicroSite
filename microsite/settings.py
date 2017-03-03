import os
from django.utils.translation import ugettext_lazy as _
import djcelery


BASE_DIR = os.path.dirname(os.path.dirname(__file__))


SECRET_KEY = ')c#(=l$5n+6xc7irx%7u(0)^%h##tj2d=v*_5#62m=o&zc_g7p'

DEBUG = True

TEMPLATE_DEBUG = DEBUG
DEBUG404 = True
ALLOWED_HOSTS = ['.micropyramid.com', 'localhost', '127.0.0.1', '.localtunnel.me']

SENTRY_ENABLED = False

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 'debug_toolbar',
    'haystack',
    'djcelery',
    'micro_admin',
    'pages',
    'micro_blog',
    'sorl.thumbnail',
    'compressor',
    'search',
    'django_simple_forum',
    'simple_pagination',
)

MIDDLEWARE_CLASSES = (
    # 'django.middleware.cache.UpdateCacheMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'microsite.middleware.LocaleMiddleware',
    # 'solid_i18n.middleware.SolidLocaleMiddleware',
    # 'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'debug_toolbar.middleware.DebugToolbarMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'htmlmin.middleware.HtmlMinifyMiddleware',
    'htmlmin.middleware.MarkRequestMiddleware',

    'microsite.middleware.RequestSessionMiddleware',
    'microsite.middleware.DetectMobileBrowser',
    'django.middleware.cache.FetchFromCacheMiddleware'
)

# SOLID_I18N_USE_REDIRECTS = True
# SOLID_I18N_HANDLE_DEFAULT_PREFIX = True
# SOLID_I18N_DEFAULT_PREFIX_REDIRECT = True
# SOLID_I18N_PREFIX_STRICT = True

HTML_MINIFY = False

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.static',
    'django.template.context_processors.request',
    'django.template.context_processors.media',
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


LANGUAGE_CODE = 'en'

LOCALE_PATHS = (
    BASE_DIR + '/locale', )

LANGUAGES = (
    ('en', _('India')),
    ('us', _('US')),
)

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


SG_USER = os.getenv('SGUSER') if os.getenv('SGUSER') else ''
SG_PWD = os.getenv('SGPWD') if os.getenv('SGPWD') else ''
SG_AUTHORIZATION = os.getenv('SGAUTHORIZATION') if os.getenv('SGAUTHORIZATION') else ''

GGL_URL_API_KEY = os.getenv('GGLAPIKEY') if os.getenv('GGLAPIKEY') else ''

GOOGLE_ANALYTICS_CODE = os.getenv('GOOGLE_ANALYTICS_CODE') if os.getenv('GOOGLE_ANALYTICS_CODE') else ''


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


# ELASTICSEARCH_DEFAULT_ANALYZER = 'synonym_analyzer'

SITE_URL = "https://micropyramid.com"

COMPRESS_ENABLED = True

COMPRESS_PRECOMPILERS = (
    ('text/less', 'lessc {infile} {outfile}'),
    ('text/x-scss', 'sass --scss {infile} {outfile}'),
)

COMPRESS_OFFLINE_CONTEXT = {
    'STATIC_URL': 'STATIC_URL',
}


if DEBUG:
    STATIC_ROOT = os.path.join(BASE_DIR, '/static')
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

COMPRESS_CSS_FILTERS = ['compressor.filters.css_default.CssAbsoluteFilter', 'compressor.filters.cssmin.CSSMinFilter']
COMPRESS_JS_FILTERS = ['compressor.filters.jsmin.JSMinFilter']
COMPRESS_REBUILD_TIMEOUT = 5400

query_cache_type = 0

# Haystack settings for Elasticsearch
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

INTERNAL_IPS = ('127.0.0.1', 'localhost', '183.82.113.154')
# DEBUG_TOOLBAR_PATCH_SETTINGS = False
# DEBUG_TOOLBAR_PANELS = [
#     'debug_toolbar.panels.versions.VersionsPanel',
#     'debug_toolbar.panels.timer.TimerPanel',
#     'debug_toolbar.panels.settings.SettingsPanel',
#     'debug_toolbar.panels.headers.HeadersPanel',
#     'debug_toolbar.panels.request.RequestPanel',
#     'debug_toolbar.panels.sql.SQLPanel',
#     'debug_toolbar.panels.staticfiles.StaticFilesPanel',
#     'debug_toolbar.panels.templates.TemplatesPanel',
#     # 'debug_toolbar.panels.cache.CachePanel',
#     'debug_toolbar.panels.signals.SignalsPanel',
#     'debug_toolbar.panels.logging.LoggingPanel',
#     'debug_toolbar.panels.redirects.RedirectsPanel',
# ]

# CACHES = {
#     'default': {
#         'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#         'LOCATION': '127.0.0.1:11211',
#     }
# }

# CACHE_MIDDLEWARE_ALIAS = 'default'  # The cache alias to use for storage.
# CACHE_MIDDLEWARE_SECONDS = 10   # The number of seconds each page should be cached.
# CACHE_MIDDLEWARE_KEY_PREFIX = 'microsite'
# CACHE_BACKEND = 'memcached://127.0.0.1:11211/'
# CACHE_IGNORE_REGEXPS = (
#     r'/admin.*',
# )
if SENTRY_ENABLED:
    if os.getenv('SENTRYDSN') is not None:
        RAVEN_CONFIG = {
            'dsn': os.getenv('SENTRYDSN'),
        }
        INSTALLED_APPS = INSTALLED_APPS + (
            'raven.contrib.django.raven_compat',
        )
        MIDDLEWARE_CLASSES = (
          'raven.contrib.django.raven_compat.middleware.Sentry404CatchMiddleware',
          'raven.contrib.django.raven_compat.middleware.SentryResponseErrorIdMiddleware',
        ) + MIDDLEWARE_CLASSES
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

# MODELTRANSLATION_DEFAULT_LANGUAGE='en'

# LOCALE_PATHS = (
#     os.path.join(BASE_DIR, 'locale'),
# )

try:
    from microsite.settings_local import *  # noqa
except ImportError as e:
    pass

