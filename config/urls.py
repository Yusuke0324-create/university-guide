from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import RedirectView
from django.conf import settings
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap

from campus_guide.sitemaps import StaticViewSitemap, BlogSitemap, OrganizationSitemap, CategorySitemap
sitemaps = {
    'static': StaticViewSitemap,
    'blog': BlogSitemap,
    'organization': OrganizationSitemap,
    'category': CategorySitemap,
}

urlpatterns = [
    path('campus_guide/', include('campus_guide.urls')),#includeはアプリ間を横断するときに使う
    #ちなみにこれはトップページ処理をcampus_guideに丸投げ
    
    path('sibuyasky1219/', admin.site.urls),#admin.site.urlsはdjangoが用意している管理画面に必要な処理の集合体
    path('', RedirectView.as_view(pattern_name='campus_guide:category_list')),#末尾に何もないurlのとき、campus_guide:category_listに転送
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}),
      #repathはパターンでurlを認識、r'^media/(?P<path>.*)$'はmediaの後に続いた文字列を全て変数pathの中に入れる
      # 画像のファイル名は常に変わるためこうしている
]