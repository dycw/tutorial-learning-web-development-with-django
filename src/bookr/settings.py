from pathlib import Path

from configurations import Configuration
from configurations.values import BooleanValue
from configurations.values import DatabaseURLValue
from configurations.values import ListValue
from configurations.values import SecretValue
from configurations.values import Value


class Dev(Configuration):
    # Build paths inside the project like this: BASE_DIR / 'subdir'.
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/4.0/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = "django-insecure-icy6)4pqc17r9(9@2r#nb2n3(*cgcra7n5@zw(jgqssr(^n1=*"  # noqa: E501, S105

    # SECURITY WARNING: don't run with debug turned on in production!
    DEBUG = BooleanValue(True)

    ALLOWED_HOSTS = ListValue([])

    # Application definition
    INSTALLED_APPS = [
        "bookr_admin.apps.BookrAdminConfig",
        "django.contrib.auth",
        "django.contrib.contenttypes",
        "django.contrib.sessions",
        "django.contrib.messages",
        "django.contrib.staticfiles",
        "rest_framework",
        "rest_framework.authtoken",
        "reviews",
    ]

    MIDDLEWARE = [
        "django.middleware.security.SecurityMiddleware",
        "django.contrib.sessions.middleware.SessionMiddleware",
        "django.middleware.common.CommonMiddleware",
        "django.middleware.csrf.CsrfViewMiddleware",
        "django.contrib.auth.middleware.AuthenticationMiddleware",
        "django.contrib.messages.middleware.MessageMiddleware",
        "django.middleware.clickjacking.XFrameOptionsMiddleware",
    ]

    ROOT_URLCONF = "bookr.urls"

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
                ]
            },
        }
    ]

    WSGI_APPLICATION = "bookr.wsgi.application"

    # Database
    # https://docs.djangoproject.com/en/4.0/ref/settings/#databases
    DATABASES = DatabaseURLValue(
        f"sqlite:///{BASE_DIR}/db.sqlite3", environ_prefix="DJANGO"
    )

    # Password validation
    # https://docs.djangoproject.com/en/4.0/ref/settings/#auth-password-validators
    AUTH_PASSWORD_VALIDATORS = [
        {
            "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"  # noqa: E501
        },
        {
            "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator"
        },
        {
            "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"
        },
        {
            "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"
        },
    ]

    # Internationalization
    # https://docs.djangoproject.com/en/4.0/topics/i18n/
    LANGUAGE_CODE = "en-us"
    TIME_ZONE = Value("UTC")
    USE_I18N = True
    USE_TZ = True

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/4.0/howto/static-files/
    STATIC_URL = "static/"
    STATICFILES_DIRS = [BASE_DIR / "static"]

    MEDIA_ROOT = BASE_DIR / "media"
    MEDIA_URL = "/media/"

    # Default primary key field type
    # https://docs.djangoproject.com/en/4.0/ref/settings/#default-auto-field
    DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"


class Prod(Dev):
    DEBUG = False
    SECRET_KEY = SecretValue()
