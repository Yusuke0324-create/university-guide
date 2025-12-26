from django.contrib.sitemaps import Sitemap
from django.urls import reverse
from .models import Blog, Organization, Category

class StaticViewSitemap(Sitemap):
    priority = 1.0
    changefreq = 'daily'
    def items(self):
        return ['campus_guide:university_list', 'campus_guide:search', 'campus_guide:site_request']
    def location(self, item):
        return reverse(item)

class BlogSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.8
    def items(self):
        return Blog.objects.all().order_by('-created_at')
    def lastmod(self, obj):
        return obj.updated_at
    def location(self, obj):
        return reverse('campus_guide:blog_detail', args=[obj.pk])

class OrganizationSitemap(Sitemap):
    changefreq = 'weekly'
    priority = 0.9
    def items(self):
        return Organization.objects.all()
    def location(self, obj):
        return reverse('campus_guide:organization_detail', args=[obj.pk])

# class CategorySitemap(Sitemap):
#     changefreq = 'weekly'
#     priority = 0.7
#     def items(self):
#         return Category.objects.all()
#     def location(self, obj):
#         return reverse('campus_guide:university_detail', args=[obj.pk])