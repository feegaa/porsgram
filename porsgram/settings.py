"""
Django settings for porsgram project.

Generated by 'django-admin startproject' using Django 3.0.7.

For more information on this file, see
https://docs.djangoproject.com/en/3.0/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/3.0/ref/settings/
"""

import os
import locale

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

TEMPLATES_DIR = BASE_DIR + '/templates'

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = '&h^6rh4eal$5(q(a)-kr22^3(5bakf$6sn40sex64#^v@1g95i'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True



ALLOWED_HOSTS = []


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # my apps
    'user.apps.UserConfig',
    'QA.apps.QaConfig',
    'django_cleanup',
    'ckeditor',
    'ckeditor_uploader',
    'rest_framework',
    'django_email_verification',
    # 'jalali_date',
]


REST_FRAMEWORK = {
    # Use Django's standard `django.contrib.auth` permissions,
    # or allow read-only access for unauthenticated users.
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.DjangoModelPermissionsOrAnonReadOnly'
    ]
}


MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'porsgram.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR,],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                "django.template.context_processors.i18n",
                "django.template.context_processors.media",
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'porsgram.wsgi.application'


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    'default': {
        'ENGINE'   : 'django.db.backends.mysql',
        'NAME'     : 'porsgram',
        'USER'     : 'porsgram',
        'PASSWORD' : '6464mysql@Porsgram',
    }
}


# Password validation
# https://docs.djangoproject.com/en/3.0/ref/settings/#auth-password-validators


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
# https://docs.djangoproject.com/en/3.0/topics/i18n/

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'UTC'

USE_I18N = True

USE_L10N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/3.0/howto/static-files/


# config auth user model
AUTH_USER_MODEL = 'user.UserModel'


# this is for redirect url after login
LOGIN_REDIRECT_URL = '/'

# this is for @login_required url
LOGIN_URL = 'user:login'


STATIC_ROOT = TEMPLATES_DIR 
STATIC_URL  = '/static/'

MEDIA_ROOT = TEMPLATES_DIR+'/media/'
MEDIA_URL  = '/media/'

CKEDITOR_UPLOAD_PATH = 'QAImage/'

STATICFILES_DIRS = [
    os.path.join(TEMPLATES_DIR, "static"),
]

# print(TEMPLATES_DIR, STATICFILES_DIRS)

CKEDITOR_CONFIGS = {
   'default': {
        # 'height': '100%',
        'width': '100%',
        'enterMode': 2,
        'filebrowserWindowHeight': 'inherit',
        'filebrowserWindowWidth': 'inherit',
        'toolbar_Full': [
            ['Bold', 'Underline', 'Strike', 'SpellChecker', 'Undo', 'Redo'],
            ['Link', 'Unlink'],
            ['Image', 'Table', 'HorizontalRule'],
            # ['TextColor', 'BGColor', 'HorizontalRule'],
            # ['Smiley', 'SpecialChar'], 
            ['Source'],
            ['JustifyLeft','JustifyCenter','JustifyRight','JustifyBlock'],
            # ['NumberedList','BulletedList'],
            # ['Indent','Outdent'],
            # ['Maximize'],
            ['CodeSnippet'],
        ],
        'extraPlugins': 'justify, liststyle, indent, codesnippet',
   },
}
CKEDITOR_ALLOW_NONIMAGE_FILES = False
MAX_UPLOAD_SIZE = "32768"
CKEDITOR_RESTRICT_BY_USER = True
CKEDITOR_LIMIT_UPLOADED_IMAGE_SIZE = 720, 840


EMAIL_BACKEND       = 'django.core.mail.backends.console.EmailBackend'
EMAIL_ACTIVE_FIELD  = 'is_active'
EMAIL_SERVER        = 'smtp.gmail.com'
EMAIL_PORT          = 587
EMAIL_ADDRESS       = 'myjoinemail@gmail.com'
EMAIL_FROM_ADDRESS  = 'myjoinemail@gmail.com'
EMAIL_PASSWORD      = 'myjoinpass' # os.environ['password_key'] suggested
EMAIL_MAIL_SUBJECT  = 'پرسگرام | تایید آدرس ایمیل'
EMAIL_MAIL_HTML     = TEMPLATES_DIR + '/email' + '/confirmEmail.html'
EMAIL_PAGE_DOMAIN   = 'http://localhost:8000/user/confirm-email/'
EMAIL_PAGE_TEMPLATE = TEMPLATES_DIR + '/user' + '/confirmEmailTemplate.html'


EMAIL_RESET_PASSWORD_HTML    = TEMPLATES_DIR + '/email' + '/resetPassword.html'
EMAIL_RESET_PASSWORD_DOMAIN  = 'http://localhost:8000/user/reset-password/'
EMAIL_RESET_PASSWORD_SUBJECT = 'پرسگرام | بازیابی گذرواژه'
EMAIL_RESET_PASSWORD_TEMPLATE = TEMPLATES_DIR + '/user' + '/resetPasswordTemplate.html'

AUTH_USER_EMAIL_UNIQUE = True



# SET LOCAL FOR JDT
# locale.setlocale(locale.LC_ALL, "fa_IR")
