# config/urls.py

from django.contrib import admin
from django.urls import path, include, re_path # re_path をインポート
from django.views.generic import RedirectView
from django.conf import settings

from django.conf.urls.static import static 
# ↓ サーブビューをインポート
from django.views.static import serve 

urlpatterns = [
    path('campus_guide/', include('campus_guide.urls')),
    path('sibuyasky1219/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='campus_guide:university_list')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    # メディアファイルを本番環境で配信するための設定
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}), 
]

# 以前の urlpatterns += static(...) の行は不要なので削除