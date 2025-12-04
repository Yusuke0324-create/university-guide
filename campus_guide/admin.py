from django.contrib import admin
from .models import Category, Organization, Blog

class OrganizationAdmin(admin.ModelAdmin):
    list_display = ('name', 'type', 'professor')
    list_filter = ('type',)

class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'organization', 'author')
    list_filter = ('categories', 'organization')
    search_fields = ('title', 'content')

admin.site.register(Category)
admin.site.register(Organization, OrganizationAdmin)
admin.site.register(Blog, BlogAdmin)