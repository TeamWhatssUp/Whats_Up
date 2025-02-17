"""
Django settings for whatsup project.

Generated by 'django-admin startproject' using Django 5.1.4.

For more information on this file, see
https://docs.djangoproject.com/en/5.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/5.1/ref/settings/
"""

from pathlib import Path


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/5.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = "django-insecure-!0&6*vmjtu)$=+o$=^!%+lnpzf5nu1qnvh&aup6rmf&@bl83k9"

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['whatsssup.com/', 'https://whatsssup.com/']


# Application definition

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "rest_framework",
    "corsheaders",
    "accounts",
    "main",
    "rest_framework_simplejwt",
]

MIDDLEWARE = [
    'whatsup.middleware.HealthCheckMiddleware',
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "corsheaders.middleware.CorsMiddleware",
]



ROOT_URLCONF = "whatsup.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "whatsup.wsgi.application"


# Database
# https://docs.djangoproject.com/en/5.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": BASE_DIR / "db.sqlite3",
    }
}


# Password validation
# https://docs.djangoproject.com/en/5.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
        'OPTIONS': {
            'min_length': 7,  # 비밀번호 최소 길이를 7자로 설정
        },
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
# https://docs.djangoproject.com/en/5.1/topics/i18n/

LANGUAGE_CODE = "ko-kr"

TIME_ZONE = "Asia/Seoul"

USE_I18N = True

USE_TZ = True


# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/5.1/howto/static-files/

STATIC_URL = "static/"

STATICFILES_DIRS = [
    BASE_DIR / "static",  # static 폴더를 정적 파일로 설정
]

# 정적 파일이 모일 디렉토리 (배포 환경에서 사용)
STATIC_ROOT = BASE_DIR / "staticfiles"

# Default primary key field type
# https://docs.djangoproject.com/en/5.1/ref/settings/#default-auto-field

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

CORS_ORIGIN_ALLOW_ALL = True

AUTH_USER_MODEL = 'accounts.CustomUser'

REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
}

from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=5),  # Access Token 유효 기간
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),   # Refresh Token 유효 기간
    'ROTATE_REFRESH_TOKENS': True,               # Refresh Token 재발급 여부
    'BLACKLIST_AFTER_ROTATION': True,             # Refresh Token 만료 처리 여부
}

# 로그인 및 로그아웃 후 이동할 경로 설정

# 로그인하지 않은 사용자가 접근 시 리디렉션될 로그인 페이지
LOGIN_URL = '/login/'  # 로그인 페이지 URL

# 로그인 성공 후 리디렉션될 페이지 (프로필 페이지로 이동)
LOGIN_REDIRECT_URL = '/profile/'  # 로그인 후 이동할 페이지

# 로그아웃 후 리디렉션될 페이지 (로그인 페이지로 이동)
LOGOUT_REDIRECT_URL = '/login/'  # 로그아웃 후 이동할 페이지

# 세션 엔진 설정 (기본값: 데이터베이스 기반 세션)
SESSION_ENGINE = 'django.contrib.sessions.backends.db'

# 세션 유지 시간 (예: 30분)
SESSION_COOKIE_AGE = 86400  # 1일(초 단위)

# 매 요청마다 세션 저장
SESSION_SAVE_EVERY_REQUEST = True

# 브라우저 닫힐 때 세션 유지 여부
SESSION_EXPIRE_AT_BROWSER_CLOSE = False

# HTTPOnly 속성 설정 (보안 강화)
SESSION_COOKIE_HTTPONLY = True

# 보안 옵션 (개발 시 False, 프로덕션에서는 True)
SESSION_COOKIE_SECURE = False

LOGGING = {
    'version': 1,
    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': 'django_debug.log',
        },
    },
    'loggers': {
        'django': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': True,
        },
    },
}

MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'

AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
]

from django.contrib.messages import constants as message_constants

MESSAGE_TAGS = {
    message_constants.DEBUG: 'debug',
    message_constants.INFO: 'info',
    message_constants.SUCCESS: 'success',
    message_constants.WARNING: 'warning',
    message_constants.ERROR: 'error',
}

CSRF_TRUSTED_ORIGINS = ['https://whatsssup.com/', 'https://whatsssup.com/']

CORS_ALLOWED_ORIGINS = ['https://whatsssup.com/', 'https://whatsssup.com/']