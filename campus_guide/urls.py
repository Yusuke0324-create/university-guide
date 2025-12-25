from django.urls import path
from . import views

app_name = 'campus_guide'

urlpatterns = [
    # トップページ
    path('', views.TopPage.as_view(), name='university_list'),
    
    # カテゴリ詳細
    path('university/<int:pk>/', views.category_detail, name='university_detail'),
    
    # 記事詳細 ★ここが重要！ name='blog_detail' に修正します
    path('blog/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog_detail'),
    
    # 検索
    path('search/', views.search_view, name='search'),
    path('request/', views.request_form_view, name='site_request'),
]