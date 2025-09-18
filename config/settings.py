# config/settings.py

import os
from pathlib import Path
from dotenv import load_dotenv
import dj_database_url

# .envファイルから環境変数を読み込む
load_dotenv()

# --- 基本設定 ---
# 1. プロジェクトのベースディレクトリを定義
BASE_DIR = Path(__file__).resolve().parent.parent

# 2. シークレットキーを環境変数から取得
SECRET_KEY = os.environ.get('SECRET_KEY')


# 本番環境かどうかを自動的に判断する
IS_PRODUCTION = 'RENDER' in os.environ
if IS_PRODUCTION:
    DEBUG = False#本番環境のほう
else:
    DEBUG = True#デバッグ環境

# 4. 許可するホストの設定
# Renderのホスト名と、ローカル開発用のホストを許可
ALLOWED_HOSTS = [
    'university-guide.onrender.com',
    '127.0.0.1',
    'localhost',
]


# --- アプリケーション定義 ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # 独自アプリケーション
    'campus_guide.apps.CampusGuideConfig',
    # サードパーティライブラリ
    'bootstrap4',
    'django_ckeditor_5',
]


# --- ミドルウェア設定 ---
# リクエスト/レスポンス処理の中間に位置する機能
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # 静的ファイル配信のために重要だから早めに設置
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# --- URL設定 ---
ROOT_URLCONF = 'config.urls'


# --- テンプレート設定 ---
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


# --- WSGI設定 ---
WSGI_APPLICATION = 'config.wsgi.application'


# --- データベース設定 ---
# RenderのDATABASE_URLを優先し、なければローカルのSQLiteを使用する
DATABASES = {
    'default': dj_database_url.config(#configの中にif文が入ってて、本番環境(DATABASE_URLある)、開発環境(DATABASE_URLない)を判断する。なかったらdefaultの値を返す。サーバー上では、PostgreSQLの接続設定を返し、defaultは無視される
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        ssl_require=IS_PRODUCTION # 本番環境でのみSSLを必須にする
    )
}


# --- パスワード検証 ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# --- 国際化対応 ---
LANGUAGE_CODE = 'ja'
TIME_ZONE = 'Asia/Tokyo'
USE_I18N = True
USE_TZ = True


# --- 静的ファイル (Static files) 設定 ---
# (CSS, JavaScript, 開発者が用意した画像など)
STATIC_URL = 'static/'
STATICFILES_DIRS = [BASE_DIR / 'static']
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'


# --- メディアファイル (Media files) 設定 ---
# (ユーザーがアップロードした画像など)
MEDIA_URL = '/media/'
# Render Diskのマウントパスを指定
MEDIA_ROOT = '/var/data/media' if IS_PRODUCTION else BASE_DIR / 'media'


# --- 主キーのデフォルト設定 ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# --- CKEditor 5 設定 ---
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
        'language': 'ja', # 日本語設定
    },
    'extends': {
        # 'extends'の設定も'default'と同じにしておくか、必要に応じてカスタマイズ
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

# --- 本番環境のみのセキュリティ設定 ---
if IS_PRODUCTION:
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_HSTS_SECONDS = 31536000
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True