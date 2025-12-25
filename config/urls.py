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
    path('campus_guide/', include('campus_guide.urls')),
    path('sibuyasky1219/', admin.site.urls),
    path('', RedirectView.as_view(pattern_name='campus_guide:university_list')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),

    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),

    re_path(r'^media/(?P<path>.*)$', serve, {'document_root': settings.MEDIA_ROOT}), 
]