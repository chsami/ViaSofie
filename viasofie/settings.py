"""
Django settings for viasofie project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 's#6!%(_6o=(x+r0(1jk!h2%$e^=*&s%*87qzg@0#xqh&k%i)di'


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = ['localhost']


# Application definition

INSTALLED_APPS = (
    'webapp',
    'captcha',
    'inplaceeditform_bootstrap',
    'inplaceeditform',
    'inplaceeditform_extra_fields',
    'bootstrap3_datetime',
    #'djng',
    #'grappelli',
    'rosetta',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'endless_pagination',
    # 'django_social_share', (outdated)
)

ADAPTOR_INPLACEEDIT = {}
if 'inplaceeditform_extra_fields' in INSTALLED_APPS:
    ADAPTOR_INPLACEEDIT['tiny'] = 'inplaceeditform_extra_fields.fields.AdaptorTinyMCEField'
    # You can add the other adaptors of inplaceeditform_extra_fields
    # https://pypi.python.org/pypi/django-inplaceedit-extra-fields#installation
if 'bootstrap3_datetime' in INSTALLED_APPS:
    ADAPTOR_INPLACEEDIT['date'] = 'inplaceeditform_bootstrap.fields.AdaptorDateBootStrapField'
    ADAPTOR_INPLACEEDIT['datetime'] = 'inplaceeditform_bootstrap.fields.AdaptorDateTimeBootStrapField'

INPLACEEDIT_EDIT_TOOLTIP_TEXT = 'Please doubleclick to edit'
INPLACEEDIT_AUTO_SAVE = True
INPLACEEDIT_EVENT = 'click'


RECAPTCHA_PUBLIC_KEY = '6Ld9RSETAAAAADhIFfv20Hmaj4eaOVpBLRHD4rY9'
RECAPTCHA_PRIVATE_KEY = '6Ld9RSETAAAAAArjY-t3DwRSUcAlLpXL8Y5Ay3Ql'
NOCAPTCHA = True

#-------------------------------------django.middleware.security.SecurityMiddleware SETTINGS --------------------------
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_HSTS_INCLUDE_SUBDOMAINS = False #if True site can only be accessed by https requests, you instruct the browser to set a timeout on your site if it isn't a https request
SECURE_HSTS_SECONDS =  0 # if integer != 0 SecurityMiddleware sets HSTS header on all responses, this is the timeout you give (read comment above)


MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    # https://docs.djangoproject.com/en/1.9/ref/middleware/ settings above
     'django.middleware.security.SecurityMiddleware',
)


TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'django.template.loaders.eggs.Loader',
    'apptemplates.Loader'
)

ROOT_URLCONF = 'viasofie.urls'
handler404 = 'mysite.views.my_custom_page_not_found_view'

WSGI_APPLICATION = 'viasofie.wsgi.application'

# pagination
from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
TEMPLATE_CONTEXT_PROCESSORS += (
    'django.core.context_processors.request',
)

ENDLESS_PAGINATION_PER_PAGE = 1;

# Database
# https://docs.djangoproject.com/en/1.7/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Internationalization
# https://docs.djangoproject.com/en/1.7/topics/i18n/
from django.utils.translation import ugettext_lazy as _

LANGUAGES = [
    ('de', _('German')),
    ('en', _('English')),
    ('fr', _('Frans')),
    ('nl', _('Nederlands')),
]
LANGUAGE_CODE = 'nl-be'
LOCALE_PATHS = (
    'webapp/locale', )

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
MEDIA_URL = '/media/'
# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.7/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'webapp/static')

AUTH_USER_MODEL = 'webapp.User'
AUTHENTICATION_BACKENDS = ['webapp.backends.EmailAuthBackend', 'django.contrib.auth.backends.ModelBackend',]

EMAIL_USE_TLS = True
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_HOST_USER = 'viasofie.groep5@gmail.com'
EMAIL_HOST_PASSWORD = 'BlackLabelZero'

DEFAULT_FROM_EMAIL = EMAIL_HOST_USER
SERVER_EMAIL = EMAIL_HOST_USER

TEMPLATES = [
{
    'BACKEND': 'django.template.backends.django.DjangoTemplates',
    'DIRS': [],
    'APP_DIRS': True,
    'OPTIONS': {
        'context_processors': [
            'django.contrib.auth.context_processors.auth',
            'django.template.context_processors.request',
        ],
    },
},
]

ROSETTA_REQUIRES_AUTH= False;

# INSTALLED_APPS += ('lockdown', )
# MIDDLEWARE_CLASSES += ('lockdown.middleware.LockdownMiddleware', )
# LOCKDOWN_PASSWORDS = ('BlackLabelZero', )
# LOCKDOWN_FORM = 'lockdown.forms.LockdownForm'

# inplaceedit
