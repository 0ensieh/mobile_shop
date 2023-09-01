"""
Django settings for config project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""

from pathlib import Path
import os

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-z0-#p3aviz71b8tdz!@ft=n6z#37+8ln0djvsh4k^$@!&h8a7d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['*']


# Application definition

INSTALLED_APPS = [
    'jazzmin',
    'clearcache', 
    'admin_persian', 
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.humanize',
    'shop.apps.ShopConfig', 
    'cart.apps.CartConfig',
    'blog.apps.BlogConfig', 
    'account.apps.AccountConfig', 
    'order.apps.OrderConfig', 
    'payment.apps.PaymentConfig',
    'tinymce',
    'widget_tweaks', 
    'crispy_forms',
    'taggit',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'cart.context_processor.cart',
                'shop.context_processor.categories', 
                'shop.context_processor.show_categories_in_footer', 
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
        }
    }


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = 'en-usa'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/


STATIC_URL = '/static/'
if DEBUG:
    STATICFILES_DIRS = [

        os.path.join(BASE_DIR, 'static')
    ]
else:
    STATIC_ROOT = os.path.join(BASE_DIR, 'static')

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


CART_SESSION_ID = 'cart'

CRISPY_TEMPLATE_PACK = 'bootstrap4' 


TINYMCE_DEFAULT_CONFIG = {

   'height': 360,
   'width': 750,
   'cleanup_on_startup': True,
   'custom_undo_redo_levels': 20,
   'selector': 'textarea',
   'theme': 'advanced',
   'plugins': '''
   textcolor save link image media preview codesample contextmenu
   table code lists fullscreen insertdatetime nonbreaking
   contextmenu directionality searchreplace wordcount visualblocks
   visualchars code fullscreen autolink lists charmap print hr
   anchor pagebreak
   ''',
   'toolbar1': '''
   fullscreen preview bold italic underline | fontselect,
   fontsizeselect | forecolor backcolor | alignleft alignright |
   aligncenter alignjustify | indent outdent | bullist numlist table |
   | link image media | codesample |
   ''',
   'toolbar2': '''
   visualblocks visualchars |
   charmap hr pagebreak nonbreaking anchor | code |
   ''',
   'contextmenu': 'formats | link image',
   'menubar': True,
   'statusbar': True,
}


LOGIN_REDIRECT_URL = 'account:profile'
LOGIN_URL = 'login'
LOGOUT_REDIRECT_URL = 'login'
AUTH_USER_MODEL = 'account.User'






MERCHANT_ID = '6f1c037a-537d-4f15-86b6-87a1001f0483'

ZARINPAL = {
    'gateway_request_url': 'https://www.zarinpal.com/pg/services/WebGate/wsdl',
    'gateway_callback_url': 'http://hamta-shop.iran.liara.run/payment/verify',
    'merchant_id': MERCHANT_ID
}

# AUTHENTICATION_BACKENDS = [
#     'django.contrib.auth.backends.ModelBackend', 
#     'account.authentication.MobileBackend'
# ]

    

EMAIL_USE_TLS = True 
EMAIL_HOST = 'smtp.gmail.com'  
EMAIL_HOST_USER = 'hamedmirzaei2001official@gmail.com'  
EMAIL_HOST_PASSWORD = 'uguktxanbhlhqjcg'  
EMAIL_PORT = 587  
DATA_UPLOAD_MAX_MEMORY_SIZE = 10242880 