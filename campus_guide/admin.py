from django.contrib import admin
from .models import Category, University, Campus, Blog

admin.site.register(Category)
admin.site.register(University)
admin.site.register(Campus)
admin.site.register(Blog)