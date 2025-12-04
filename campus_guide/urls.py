from django.urls import path
from . import views

app_name = 'campus_guide'

urlpatterns = [
    # トップページ
    path('', views.TopPage.as_view(), name='university_list'),
    
    # カテゴリ詳細（旧 大学詳細）
    # クラス(as_view)ではなく関数になったので注意
    path('university/<int:pk>/', views.category_detail, name='university_detail'),
    
    # 記事詳細
    path('blog/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog_post_detail'),
    
    # 検索
    path('search/', views.search_view, name='search'),
]