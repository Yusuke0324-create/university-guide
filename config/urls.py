from django.contrib import admin
from django.urls import path, include, re_path, reverse
from django.views.generic import RedirectView
from django.conf import settings
from django.views.static import serve
from django.contrib.sitemaps.views import sitemap
from django.contrib.sitemaps import Sitemap

# サイトマップ設定
class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'

    def items(self):
        return ['campus_guide:university_list', 'campus_guide:search']

    def location(self, item):
        return reverse(item)

sitemaps = {
    'static': StaticViewSitemap,
}

# URL
urlpatterns = [
    path('campus_guide/', include('campus_guide.urls')),
    path('sibuyasky1219/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='campus_guide:university_list')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    # サイトマップ
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    # メディアファイル配信
    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}), 
]