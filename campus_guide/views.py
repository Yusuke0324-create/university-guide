from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Q, Count
# ★新しいモデルをインポート
from .models import Category, Organization, Blog

# 1. トップページ
# 1. トップページ
class TopPage(generic.ListView):
    model = Category
    template_name = 'app_folder/university_list.html'
    context_object_name = 'categories' 
    
    def get_queryset(self):
        # カテゴリを表示順に並べる
        return Category.objects.order_by('order')

    # ↓↓↓ このメソッドが抜けていました！これを追加してください ↓↓↓
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        # 団体（Organization）を、記事（blog_set）の数が多い順に並べ替える
        # ※もしエラーが出る場合は 'blog_set' を 'blog' に変えてみてください
        context['ranking_orgs'] = Organization.objects.annotate(
            num_posts=Count('blog')
        ).order_by('-num_posts')[:6]
        
        return context

    

# 2. カテゴリ詳細ページ（旧 大学詳細ページ）
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    # そのカテゴリの記事を取得
    blogs = category.blogs.all().order_by('-created_at')
    
    return render(request, 'app_folder/university_detail.html', {
        'university': category, # テンプレートに合わせて変数名を偽装
        'blogs': blogs,
    })

# 3. 記事詳細ページ
class BlogPostDetailView(generic.DetailView):
    model = Blog
    template_name = 'app_folder/blog_post_detail.html'
    context_object_name = 'blog_post'

# 4. 検索機能
def search_view(request):
    query = request.GET.get('keyword')
    results = []

    if query:
        results = Blog.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(organization__name__icontains=query)
        ).distinct().order_by('-created_at')

    return render(request, 'app_folder/search_results.html', {
        'query': query,
        'results': results,
    })