import os

APP_SETTINGS = None

ADMINS = (
    ('img', 'img@it-solution.ru'),
)

BASE_DOMAIN = 'https://is_demo.it-solution.ru'
DOMAIN = "vervet-top-manually.ngrok-free.app"

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_PATH = os.path.dirname(__file__).replace('\\','/')

SECRET_KEY = 'UxWXNk8hFEJYUkstPtBdtNgvqKfOFbME'

DEBUG = False

ALLOWED_HOSTS = []

INSTALLED_APPS = [
    'intern.select_user',
    'intern.move_deadline',
    'intern.robot_vacancies',
    'intern.powerbi',
    'intern.send_msg_tg_bot',
    'intern.openai_voice_recognition',
    'intern.field_sort',
    'intern.import_table_to_bitrix',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'post_currency',

    'integration_utils.bitrix24',
    'integration_utils.its_utils.app_gitpull',
    'start',
    'tasks',
    'ones_fresh_unf_with_b24',
    'crmfields',
    'callsuploader',
    'duplicatefinder',
    'usermanager',
    'selectuser',
    'company_on_map',
    'employeegrid',
    'robot_currency',
    'allcompbizproc',
    'product_list_excel',
    'import_company_google',
    'demo_data_in_bitrix',
    "sample_tg_bot",
    'audio_recognition',
    'calls_to_telegram',
    'best_call_manager',
    'tg_openai_bot',
    'deal_for_powerbi',
    'autocomplete_crm_tasks',
    'move_tasks_deadline_js',
    "company_to_db.apps.CompanyToDbConfig"
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
]

ROOT_URLCONF = 'urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')]
        ,
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

WSGI_APPLICATION = 'wsgi.application'


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'foodgram',
        'USER': 'postgresql',
        'PASSWORD': '123456',
        'HOST': 'localhost',
        'PORT': '5432',
    },
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


LANGUAGE_CODE = 'ru-ru'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_L10N = True

USE_TZ = True

MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
ENTRY_FILE_UPLOADING_FOLDER = os.path.join(MEDIA_ROOT, 'uploaded_entrie_files')

STATIC_ROOT = os.path.join(BASE_DIR, 'static')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = '/static/admin/'
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
)
STATICFILES_DIRS = [
     os.path.join(BASE_DIR, 'staticfiles'),
]


from integration_utils.its_utils.mute_logger import MuteLogger
ilogger = MuteLogger()



# local settings
try:
    from local_settings import *
except ImportError:
    from warnings import warn

    warn('create local_settings.py')

if not APP_SETTINGS:
    from integration_utils.bitrix24.local_settings_class import LocalSettingsClass
    APP_SETTINGS = LocalSettingsClass(
        # portal_domain='',
        app_domain='is_demo.it-solution.ru',
        app_name='post_currency',
        salt='df897hynj4b34u804b5n45bkl4b',
        secret_key='sfjbh40989034nk4j4389tfj',
        # application_bitrix_client_id='',
        # application_bitrix_client_secret='',
        application_index_path='/',
    )

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
