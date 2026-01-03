import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url
from django.shortcuts import redirect

#環境変数読み込み
load_dotenv()

#基本設定
BASE_DIR = Path(__file__).resolve().parent.parent
SECRET_KEY = os.environ.get('SECRET_KEY')

#環境判定
IS_PRODUCTION = 'RENDER' in os.environ
if IS_PRODUCTION:
    DEBUG = False
else:
    DEBUG = True

#許可ホスト
ALLOWED_HOSTS = [
    'university-guide.onrender.com',
    '127.0.0.1',
    'localhost',
    'canvas-compass.net',
    'www.canvas-compass.net',
]


#アプリケーション定義
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    #サイトマップ用設定
    'django.contrib.sites',
    'django.contrib.sitemaps',
    #独自アプリケーション
    'campus_guide.apps.CampusGuideConfig',
    #サードパーティ
    'bootstrap4',
    'django_ckeditor_5',
]


#ミドルウェア
MIDDLEWARE = [
    'config.settings.redirect_to_custom_domain', 
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


#URL設定
ROOT_URLCONF = 'config.urls'


#テンプレート
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


#WSGI
WSGI_APPLICATION = 'config.wsgi.application'


#データベース
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        ssl_require=IS_PRODUCTION
    )
}


#パスワード検証
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


#言語・タイムゾーン
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True


#静的ファイル
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


#メディアファイル
MEDIA_URL = '/media/'
MEDIA_ROOT = '/var/data/media' if IS_PRODUCTION else BASE_DIR / 'media'


#主キー設定
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


#CKEditor設定
CKEDITOR_5_UPLOAD_PATH = "uploads/ckeditor5/"
CKEDITOR_5_CONFIGS = {
    'default': {
        'toolbar': [
            'heading', '|',
            'bold', 'italic', 'underline', 'strikethrough', '|',
            'bulletedList', 'numberedList', 'blockQuote', '|',
            'link', 'imageUpload', 'insertTable', 'mediaEmbed', '|',
            'alignment', '|',
            'undo', 'redo',
        ],
        'image': {
            'toolbar': [
                'imageStyle:inline', 'imageStyle:block', 'imageStyle:side', '|',
                'toggleImageCaption', 'imageTextAlternative'
            ]
        },
        'table': {
            'contentToolbar': [
                'tableColumn', 'tableRow', 'mergeTableCells'
            ]
        },
        'language': 'ja',
    },
    'extends': {
        'toolbar': [
            'heading', '|',
            'bold', 'italic', 'underline', 'strikethrough', '|',
            'bulletedList', 'numberedList', 'blockQuote', '|',
            'link', 'imageUpload', 'insertTable', 'mediaEmbed', '|',
            'alignment', '|',
            'undo', 'redo',
        ],
        'language': 'ja',
    }
}


#セキュリティ設定（本番環境）
if IS_PRODUCTION:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True

#サイトID（Sitemap用）
SITE_ID = 1


CSRF_TRUSTED_ORIGINS = [
    'https://university-guide.onrender.com',
    'https://canvas-compass.net',
    'https://www.canvas-compass.net',
]





def redirect_to_custom_domain(get_response):#get_responseはミドルウェア的に最初に行う処理
    def middleware(request):#requestはサイト訪問者の情報
        host = request.get_host()
        if 'onrender.com' in host:
            return redirect(f'https://canvas-compass.net{request.path}', permanent=True)
        return get_response(request)
    return middleware