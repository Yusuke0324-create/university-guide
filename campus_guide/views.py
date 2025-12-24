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
        #カテゴリを表示順に並べる
        return Category.objects.order_by('order')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        #記事数の多い団体上位6つを取得
        context['ranking_orgs'] = Organization.objects.annotate(
            num_posts=Count('blog')
        ).order_by('-num_posts')[:6]
        return context

#カテゴリ詳細ページ
def category_detail(request, pk):
    category = get_object_or_404(Category, pk=pk)
    #優先度順、次に作成日順で並び替え
    blogs = category.blogs.all().order_by('-priority', '-created_at')
    
    return render(request, 'app_folder/university_detail.html', {
        'university': category, #テンプレート側の変数名に合わせています
        'blogs': blogs,
    })

#記事詳細ページ
class BlogPostDetailView(generic.DetailView):
    model = Blog
    template_name = 'app_folder/blog_post_detail.html'
    context_object_name = 'blog_post'

#検索機能
def search_view(request):
    query = request.GET.get('keyword')
    results = []

    if query:
        results = Blog.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(organization__name__icontains=query)
        ).distinct().order_by('-priority', '-created_at')

    return render(request, 'app_folder/search_results.html', {
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