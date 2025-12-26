from django.urls import path
from . import views

app_name = 'campus_guide'

urlpatterns = [
    #トップページ
    path('', views.TopPage.as_view(), name='category_list'),
    
    #カテゴリ詳細
    path('category/<int:pk>/', views.category_detail, name='category_detail'),
    
    #記事詳細
    path('blog/<int:pk>/', views.BlogPostDetailView.as_view(), name='blog_detail'),
    
   

    #検索
    path('search/', views.search_view, name='search'),
    path('request/', views.request_form_view, name='site_request'),
    path('organization/<int:pk>/', views.organization_detail, name='organization_detail'),
]