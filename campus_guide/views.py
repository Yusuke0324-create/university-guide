from django.shortcuts import render, get_object_or_404
from django.views import generic
from django.db.models import Q, Count
from .models import Category, Organization, Blog
from .forms import CommentForm, SiteRequestForm

#トップページ
class TopPage(generic.ListView):
    model = Category
    template_name = 'app_folder/university_list.html'
    context_object_name = 'categories' 
    
    def get_queryset(self):
        return Category.objects.order_by('order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        #人気記事ランキング
        context['ranking_blogs'] = Blog.objects.order_by('-views')[:5]
        
        #団体ランキング
        context['ranking_orgs'] = Organization.objects.annotate(
            num_posts=Count('blog')
        ).order_by('-num_posts')[:6]
        
        return context

#カテゴリ詳細ページ
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    blogs = category.blogs.all().order_by('-priority', '-created_at')
    
    return render(request, 'app_folder/university_detail.html', {
        'category': category,
        'blogs': blogs,
    })

#記事詳細ページ
class BlogPostDetailView(generic.DetailView):
    model = Blog
    template_name = 'app_folder/blog_post_detail.html'
    context_object_name = 'blog_post'

    def get_object(self, queryset=None):
        obj = super().get_object(queryset)
        obj.views += 1
        obj.save()
        return obj

#団体詳細ページ
def organization_detail(request, pk):
    organization = get_object_or_404(Organization, pk=pk)
    #その団体に関連する記事を取得
    blogs = Blog.objects.filter(organization=organization).order_by('-priority', '-created_at')
    
    return render(request, 'app_folder/organization_detail.html', {
        'organization': organization,
        'blogs': blogs,
    })

#検索機能
def search_view(request):
    query = request.GET.get('keyword')#入力フォームからの検索キーワード受け取り
    results = []

    if query:
        results = Blog.objects.filter(
            Q(title__icontains=query) | #タイトルにキーワードが含まれているか
            Q(content__icontains=query) |#記事内容
            Q(organization__name__icontains=query)#団体名
        ).distinct().order_by('-priority', '-created_at')

    return render(request, 'app_folder/search_results.html', {#return render(受け取った第一引数,表示させたいHTML,渡したい変数)
        'query': query,
        'results': results,
    })

#要望フォーム
def request_form_view(request):
    if request.method == 'POST':
        form = SiteRequestForm(request.POST)
        if form.is_valid():
            form.save()
            return render(request, 'app_folder/request_done.html')
    else:
        form = SiteRequestForm()

    return render(request, 'app_folder/request_form.html', {'form': form})