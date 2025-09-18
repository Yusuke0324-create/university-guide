from django.contrib import admin

# Register your models here.
from .models import Category, University,Blog

admin.site.register(Category)
admin.site.register(University)
admin.site.register(Blog)
