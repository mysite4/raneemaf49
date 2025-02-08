import os
from pathlib import Path
import dj_database_url
from decouple import config

SECRET_KEY = config('SECRET_KEY')

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.2/howto/deployment/checklist/



# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

SECURE_SSL_REDIRECT = True

ALLOWED_HOSTS = ['192.168.0.109', '127.0.0.1', 'localhost']


AUTH_USER_MODEL = 'user_management.CustomUser'

# Application definition

INSTALLED_APPS = [
    'user_management',
    'pages.apps.PagesConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'project.urls'

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
            ],
        },
    },
]

WSGI_APPLICATION = 'project.wsgi.application'

DATABASES = {
    'default': dj_database_url.config(default=os.getenv("DATABASE_URL"))
}
# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',  # استخدام محرك MySQL
        'NAME': 'new',  # اسم قاعدة البيانات التي أنشأتها
        'USER': 'root',  # اسم المستخدم (عادة يكون 'root' إذا لم تكن قد أنشأت مستخدم آخر)
        'PASSWORD': '',  # إذا لم يكن لديك كلمة مرور اتركها فارغة
        'HOST': 'localhost',  # المضيف (localhost يعني أن القاعدة على جهازك المحلي)
        'PORT': '3306',  # المنفذ الافتراضي ل MySQL
   }
 }


# Password validation
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
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True


# Static files (CSS, JavaScript, Images)
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
STATICFILES_DIRS = [os.path.join(BASE_DIR, 'project/static')]

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Media files (Uploaded files like books)
MEDIA_URL = '/media/'

# تأكد من أن BASE_DIR من النوع Path
BASE_DIR = Path(__file__).resolve().parent.parent

# تعديل MEDIA_ROOT لاستخدام BASE_DIR بشكل صحيح
MEDIA_ROOT = BASE_DIR / 'media'


# Authentication URLs
LOGIN_URL = '/admin-panel/login/'
LOGOUT_REDIRECT_URL = '/admin-panel/login/'
