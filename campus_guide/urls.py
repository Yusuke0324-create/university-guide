# campus_guide/urls.py

from django.urls import path
from . import views

app_name = 'campus_guide'

urlpatterns = [
    # 1. トップページ (大学一覧)
    path('', views.TopPage.as_view(), name='university_list'),
    
    # 2. 大学詳細ページ (キャンパス一覧)
    path('university/<int:pk>/', views.UniversityDetailView.as_view(), name='university_detail'),
    
    # 3. キャンパス詳細ページ (ブログ一覧)
    path('campus/<int:pk>/', views.CampusDetailView.as_view(), name='campus_detail'),
    
    # 4. ブログ記事詳細ページ
    path('blog/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog_post_detail'),
    
    # 5. 検索結果ページ
    path('search/', views.search_view, name='search'),
# カッコなしで、「この関数を使ってね」と伝えるのが正解です
]