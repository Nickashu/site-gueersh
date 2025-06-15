from pathlib import Path
import os
from dotenv import load_dotenv
from django.contrib import messages
import dj_database_url

load_dotenv()  # loads the configs from .env

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.getenv("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = os.getenv("DEBUG", "True") == "True"

ALLOWED_HOSTS = os.getenv("ALLOWED_HOSTS").split(",")

CSRF_TRUSTED_ORIGINS = os.getenv("CSRF_TRUSTED_ORIGINS").split(",")

MEDIA_URL = '/media/'
MEDIA_ROOT = os.getenv("RAILWAY_VOLUME_MOUNT_PATH", BASE_DIR / 'media')

# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'base.apps.BaseConfig',   #app criado para o site base
    
    # Aplicativos do Django Allauth
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    
    'django_summernote',   #Editor de texto enriquecido para os posts
    
    'crispy_forms',  #Para formulários mais bonitos e funcionais
    'crispy_bootstrap5',  #Para usar o Bootstrap 5 com o Crispy Forms
]

#Configurações do Crispy Forms:
CRISPY_ALLOWED_TEMPLATE_PACKS = ("bootstrap5",)
CRISPY_TEMPLATE_PACK = "bootstrap5"

SITE_ID = 1  

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',  #Middleware para servir arquivos estáticos em produção
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    
    "allauth.account.middleware.AccountMiddleware",

    'base.middleware.ClearMessagesInAdminMiddleware',   #Middleware personalizado para limpar mensagens no admin
]

STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'    #Armazena arquivos estáticos comprimidos e com manifesto para produção

ROOT_URLCONF = 'gueersh_project.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
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

WSGI_APPLICATION = 'gueersh_project.wsgi.application'


if DEBUG:
    DATABASES = {
        'default': {
            'ENGINE': os.getenv("DB_ENGINE", 'django.db.backends.postgresql_psycopg2'),
            'NAME': os.getenv("DB_NAME"),
            'USER': os.getenv("DB_USER"),
            'PASSWORD': os.getenv("DB_PASSWORD"),
            'HOST': os.getenv("DB_HOST"),
            'PORT': os.getenv("DB_PORT"),
        }
    }
else:   #Configuração para produção usando dj_database_url
    DATABASES = {
        'default': dj_database_url.parse(os.getenv("DATABASE_URL"), conn_max_age=600)
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


# Internationalization

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

if DEBUG:
    USE_TZ = True
else:
    USE_TZ = False    #Desabilita o uso de timezone em produção para evitar problemas com o banco de dados


# Static files (CSS, JavaScript, Images)

STATIC_URL = '/static/'   #URL para acessar os arquivos estáticos
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')   #Diretório onde os arquivos estáticos serão coletados após o comando collectstatic

# Default primary key field type

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#Configurações do Django Allauth
AUTHENTICATION_BACKENDS = (
    'django.contrib.auth.backends.ModelBackend',
    'allauth.account.auth_backends.AuthenticationBackend',
)


#Configurações do Django Allauth:
LOGIN_REDIRECT_URL = '/'  # URL para redirecionar após o login
LOGOUT_REDIRECT_URL = '/'  # URL para redirecionar após o logout
ACCOUNT_LOGOUT_ON_GET = True    # Permite logout via GET request (não precisa ter página de logout)
ACCOUNT_SIGNUP_FIELDS = ['email*', 'username*', 'password1*', 'password2*']
ACCOUNT_LOGIN_METHODS = {'username', 'email'}  # Método de autenticação (pode ser username, email ou ambos)

ACCOUNT_EMAIL_VERIFICATION = "mandatory"   #Faz com que o email precise ser verificado antes de permitir o login
ACCOUNT_CONFIRM_EMAIL_ON_GET = True  #Confirma ao clicar no link, sem botão extra
ACCOUNT_SESSION_REMEMBER = False #Desabilita a opção de lembrar a sessão (não armazena cookies de sessão) 
ACCOUNT_UNIQUE_EMAIL = True  #Garante que o email seja único (não pode haver dois usuários com o mesmo email)
#ACCOUNT_EMAIL_CONFIRMATION_EXPIRE_DAYS = 0.0007  #Teste rápido de expiração do email de confirmação (1 minuto)

#Formulários personalizados:
ACCOUNT_FORMS = {
    'signup': 'base.forms.CustomSignupForm',  # ajuste para seu app
}

AUTH_PASSWORD_VALIDATORS = [     #Validações de senha
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator', 'OPTIONS': {'min_length': 6},},
]


#Configurações de email
#EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'   #Para desenvolvimento, exibe os emails no console
EMAIL_BACKEND = os.getenv("EMAIL_BACKEND", "django.core.mail.backends.smtp.EmailBackend")
EMAIL_HOST = os.getenv("EMAIL_HOST", "smtp.gmail.com")
EMAIL_PORT = int(os.getenv("EMAIL_PORT", 587))
DEFAULT_FROM_EMAIL = os.getenv("DEFAULT_FROM_EMAIL", "Meu Site")
EMAIL_USE_TLS = os.getenv("EMAIL_USE_TLS", "True") == "True"
EMAIL_HOST_USER = os.getenv("EMAIL_HOST_USER")
EMAIL_HOST_PASSWORD = os.getenv("EMAIL_HOST_PASSWORD")

#Configurações do site
SITE_URL = os.getenv("SITE_URL", "http://localhost:8000")  # URL do site, usada para links em emails



#Configurações do Summernote:
SUMMERNOTE_CONFIG = {
    'iframe': True,
    'summernote': {
        'toolbar': [
            ['style', ['style']],
            ['font', ['bold', 'italic', 'underline', 'clear']],
            ['fontname', ['fontname']],
            ['fontsize', ['fontsize']],
            ['color', ['color']],
            ['para', ['ul', 'ol', 'paragraph']],
            ['height', ['height']],
            ['table', ['table']],
            ['insert', ['picture', 'link', 'video', 'hr']],
            ['view', ['fullscreen', 'codeview', 'help']],
        ],
        'width': '100%',
        'height': '500px',
    },
}

MESSAGE_TAGS = {
    messages.ERROR: 'danger',  # transforma 'error' em 'danger'
}