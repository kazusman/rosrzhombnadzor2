import os
import json

from pathlib import Path
from dotenv import load_dotenv
from celery.schedules import crontab


load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = os.getenv('SECRET_KEY')

DEBUG = int(os.getenv('DEBUG'))

ALLOWED_HOSTS = os.getenv('ALLOWED_HOSTS').split()

INSTALLED_APPS = [
    'jazzmin.apps.JazzminConfig',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'bot.apps.BotConfig',
    'google_vision.apps.GoogleVisionConfig'
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

ROOT_URLCONF = 'app.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
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

WSGI_APPLICATION = 'app.wsgi.application'

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': os.getenv('DATABASE'),
        'USER': os.getenv('USER'),
        'PASSWORD': os.getenv('PASSWORD'),
        'HOST': os.getenv('HOST'),
        'PORT': os.getenv('PORT')
    }
}

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

LANGUAGE_CODE = 'en-us'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

STATIC_URL = '/static/'

CHAT_ID = int(os.getenv('CHAT_ID'))
TELEGRAM_BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
PROJECT_URL = os.getenv('PROJECT_URL')
CHAT_URL = os.getenv('CHAT_URL')

BOOLEAN_CHOICES = [
    (True, '✅ Yes'),
    (False, '❌ No')
]

GMAIL_CREDENTIALS = {
    'type': os.getenv('TYPE'),
    'project_id': os.getenv('PROJECT_ID'),
    'private_key_id': os.getenv('PRIVATE_KEY_ID'),
    'private_key': os.getenv('PRIVATE_KEY'),
    'client_email': os.getenv('CLIENT_EMAIL'),
    'client_id': os.getenv('CLIENT_ID'),
    'auth_uri': os.getenv('AUTH_URI'),
    'token_uri': os.getenv('TOKEN_URI'),
    'auth_provider_x509_cert_url': os.getenv('AUTH_PROVIDER_X509_CERT_URL'),
    'client_x509_cert_url': os.getenv('CLIENT_X509_CERT_URL')
}

GOOGLE_CREDENTIALS_FILE_PATH = os.path.join(BASE_DIR, 'creds.json')


def create_google_credentials_file():

    if os.path.exists(GOOGLE_CREDENTIALS_FILE_PATH):
        return
    else:
        with open(GOOGLE_CREDENTIALS_FILE_PATH, 'w') as file:
            json.dump(GMAIL_CREDENTIALS, file)


create_google_credentials_file()

CELERY_TIMEZONE = TIME_ZONE
CELERY_TASK_TRACK_STARTED = True
CELERY_BROKER_URL = os.getenv('CELERY_BROKER_URL')
CELERY_BEAT_SCHEDULE = {
    'monthly_coins': {
        'task': 'bot.tasks.give_monthly_coins',
        'schedule': crontab(day_of_month=1, hour=12, minute=0)

    },
    'happy_birthday': {
        'task': 'bot.tasks.send_happy_birthday',
        'schedule': crontab(hour=12, minute=0)
    }
}

# Jazzmin settings

JAZZMIN_SETTINGS = {
    "site_title": "РосРжомбНадзор",
    "site_header": "РосРжомбНадзор",
    "site_logo": 'jazzmin/img/logo.png',
    "site_icon": "jazzmin/img/favicon.ico",
    "welcome_sign": "Добро пожаловать в РосРжомбНадзор",
    "copyright": 'РЖАКА РЖОМБА РЖУЛЬКА',
    "user_avatar": None,
    "search_model": None,
    "topmenu_links": [

        {"name": "Home",  "url": "/admin"},

        {"name": "Open bot", "url": os.getenv('BOT_URL'), "new_window": True},

        {"name": "Open chat", "url": os.getenv('CHAT_URL'), "new_window": True},

        {"name": 'Set webhook', "url": f"/bot/set_webhook/"},

        {"app": "bot"},
    ],
    "usermenu_links": None,
    "show_sidebar": True,
    "navigation_expanded": False,
    "hide_apps": [],
    "hide_models": [],
    "order_with_respect_to": ['bot', 'google_vision'],
    "custom_links": {
        "bot": [{
            "name": "Set webhook",
            "url": "/bot/set_webhook",
            "icon": "fas fa-sync-alt",
            "new_window": True,
        }]
    },
    # https://fontawesome.com/v5.15/icons?d=gallery&p=2&v=5.0.0,5.0.1,5.0.10,5.0.11,5.0.12,5.0.13,5.0.2,5.0.3,5.0.4,5.0.5,5.0.6,5.0.7,5.0.8,5.0.9,5.1.0,5.1.1,5.2.0,5.3.0,5.3.1,5.4.0,5.4.1,5.4.2,5.13.0,5.12.0,5.11.2,5.11.1,5.10.0,5.9.0,5.8.2,5.8.1,5.7.2,5.7.1,5.7.0,5.6.3,5.5.0,5.4.2&m=free
    "icons": {
        "auth": "fas fa-users-cog",
        "auth.user": "fas fa-user",
        "auth.Group": "fas fa-users",
        "bot": "fas fa-robot",
        "bot.user": "fas fa-user-circle",
        "bot.message": "fas fa-comment-dots",
        "bot.funnyaction": "far fa-laugh-squint",
        "bot.bet": "fas fa-dice",
        "bot.notfoundanswer": "fas fa-question",
        "bot.startanswer": "fas fa-play",
        "bot.status": "fas fa-link",
        "google_vision": "fab fa-google",
        "google_vision.request": "fas fa-globe"

    },
    "default_icon_parents": "fas fa-chevron-circle-right",
    "default_icon_children": "fas fa-circle",
    "related_modal_active": False,
    "custom_css": None,
    "custom_js": None,
    "show_ui_builder": False,
    "changeform_format": "horizontal_tabs",
    "changeform_format_overrides": None,
    "language_chooser": False,
}

JAZZMIN_UI_TWEAKS = {
    "navbar_small_text": False,
    "footer_small_text": False,
    "body_small_text": False,
    "brand_small_text": False,
    "brand_colour": "navbar-lightblue",
    "accent": "accent-primary",
    "navbar": "navbar-lightblue navbar-dark",
    "no_navbar_border": True,
    "navbar_fixed": True,
    "layout_boxed": False,
    "footer_fixed": False,
    "sidebar_fixed": True,
    "sidebar": "sidebar-light-primary",
    "sidebar_nav_small_text": False,
    "sidebar_disable_expand": False,
    "sidebar_nav_child_indent": True,
    "sidebar_nav_compact_style": True,
    "sidebar_nav_legacy_style": False,
    "sidebar_nav_flat_style": True,
    "theme": "default",
    "dark_mode_theme": None,
    "button_classes": {
        "primary": "btn-outline-primary",
        "secondary": "btn-outline-secondary",
        "info": "btn-outline-info",
        "warning": "btn-outline-warning",
        "danger": "btn-outline-danger",
        "success": "btn-outline-success"
    },
    "actions_sticky_top": False
}