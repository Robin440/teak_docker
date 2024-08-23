from pathlib import Path
import os


BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = "django-insecure-81s$xokgzcu1o^03w*2^e61a3v-a%mj^h#qk@5vsw3plke119^"

DEBUG = True

ALLOWED_HOSTS = [
    "13.201.129.29"
    "13.211.164.13",
    "localhost",
    "127.0.0.1",
    "3.27.61.24",
    "54.153.175.73",
    "api.ipify.org",
    "www.shadowserver.org",
    ".vercel.app",
    "6d37-36-255-87-0.ngrok-free.app",
    "stirred-monkfish-luckily.ngrok-free.app",
]


INSTALLED_APPS = [
    # custom interface-
    "admin_interface",
    "colorfield",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "accounts",
    "teak_admin",
    "product",
    "django_cleanup.apps.CleanupConfig",
    "drf_yasg"
]


X_FRAME_OPTIONS = "SAMEORIGIN"
SILENCED_SYSTEM_CHECKS = ["security.W019"]

MIDDLEWARE = [
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "core.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

WSGI_APPLICATION = "core.wsgi.application"

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": "teak_db",
        "USER": "postgres",
        "HOST": "t_db",
        "PORT": "5432",
        "PASSWORD": "root",
    }
}

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]

LANGUAGE_CODE = "en-us"
TIME_ZONE = "UTC"
USE_I18N = True
USE_TZ = True

STATIC_URL = "/static/"
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"
AUTH_USER_MODEL = "accounts.CustomUser"


CORS_ALLOW_HEADERS = [
    "accept",
    "authorization",
    "content-type",
    "user-agent",
    "x-csrftoken",
    "x-requested-with",
    "ngrok-skip-browser-warning",
]

CORS_ALLOW_METHODS = [
    "DELETE",
    "GET",
    "OPTIONS",
    "PATCH",
    "POST",
    "PUT",
]

# Allow requests from all origins (for development purposes)
CORS_ALLOW_ALL_ORIGINS = True

# Optional: If you want to whitelist specific origins, use this instead:
CORS_ORIGIN_WHITELIST = [
    "http://127.0.0.1:3000",
    "http://localhost:3000",
    "http://localhost:3001",
    "http://127.0.0.1:3001",
    # Add other allowed origins here
]


# Allow credentials (cookies, authentication headers, etc.)
CORS_ALLOW_CREDENTIALS = True


CSRF_TRUSTED_ORIGINS = [
    "http://localhost:3000",
    "http://localhost:3001",
    "https://6d37-36-255-87-0.ngrok-free.app",
    "https://stirred-monkfish-luckily.ngrok-free.app",
]


# settings.py
CKEDITOR_UPLOAD_PATH = "uploads/"
CKEDITOR_CONFIGS = {
    "default": {
        "toolbar": "full",
        "height": 300,
        "width": 800,
    },
}



# log files



LOGS_DIR = os.path.join(BASE_DIR, "logs")
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)


# Define file names for handlers
handlers_filename = ["app", "django_request"]

# Define handlers for each file name
handlers = {}
for file_name in handlers_filename:
    # Define TimedRotatingFileHandler for rotating log files based on time
    handlers[file_name] = {
        'class': 'logging.handlers.TimedRotatingFileHandler',  # Specifies the handler class
        'filename': f'logs/{file_name}.log',  # Specifies the log file name and path
        'level': 'DEBUG',  # Sets the logging level to DEBUG
        'when': 'D',  # Specifies the time unit for rotation (D = day)
        'interval': 30,  # Specifies the interval for rotation (30 days)
        'backupCount': 1,  # Specifies the number of backup files to keep before deletion
        'formatter': 'verbose'  # Specifies the formatter for log messages
    }

# Define loggers for each file name
loggers = {}
for file_name in handlers_filename:
    # Define logger configuration for each log file
    loggers[file_name] = {
        'handlers': [file_name],  # Specifies the handler(s) for the logger
        'level': 'DEBUG',  # Sets the logging level to DEBUG
    }

# Construct the simplified LOGGING configuration dictionary
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'handlers': handlers,  # Specifies the handlers defined earlier
    'loggers': loggers,  # Specifies the loggers defined earlier
    'formatters': {
        'verbose': {'format': '%(levelname)s %(asctime)s | %(message)s'},  # Specifies the format for verbose logs
        'simple': {'format': '%(levelname)s %(message)s'},  # Specifies the format for simple logs
    },
    'root': {
        'handlers': handlers_filename,  # Specifies the root handlers
        'level': 'DEBUG',  # Sets the root logging level to DEBUG
    },
}