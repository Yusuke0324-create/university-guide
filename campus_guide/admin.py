from django.contrib import admin
from .models import Category, Organization, Blog, Comment, SiteRequest

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

@admin.register(SiteRequest)
class SiteRequestAdmin(admin.ModelAdmin):
    list_display = ('content', 'name', 'email', 'created_at', 'is_read') # 一覧で見たい項目
    list_filter = ('is_read', 'created_at') # フィルター機能
    search_fields = ('content', 'name') # 検索機能
    readonly_fields = ('created_at',) # 日付は書き換え不可に