# campus_guide/urls.py

from django.urls import path
from . import views

app_name = 'campus_guide'

urlpatterns = [
    path('', views.top_page, name='top_page'),
    path('search/', views.search_view, name='search'),
    path('detail/<int:pk>/', views.detail_page, name='detail_page'),
    path('blog/<int:pk>/', views.blog_post_detail_view, name='blog_post_detail'),
]