from django.shortcuts import render
from django.views import View, generic
from .models import University, Campus, Blog
from django.db.models import Q

# 1. トップページ：カテゴリ（旧University）一覧を表示
class TopPage(generic.ListView):
    model = University
    template_name = 'app_folder/university_list.html'
    context_object_name = 'universities'
    paginate_by = 6
    
    # 登録順（ID順）に並べる設定を追加しておくと表示が安定します
    def get_queryset(self):
        return University.objects.order_by('id')

# 2. カテゴリ詳細ページ：記事一覧を直接表示（ロジック変更なし）
class UniversityDetailView(generic.DetailView):
    model = University
    template_name = 'app_folder/university_detail.html'
    context_object_name = 'university'

# 3. キャンパス詳細ページ（今回は使わないが残しておく）
class CampusDetailView(generic.DetailView):
    model = Campus
    template_name = 'app_folder/campus_detail.html'
    context_object_name = 'campus'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = self.object.blogs.all().order_by('-created_at')
        return context

# 4. ブログ詳細ページ
class BlogPostDetailView(generic.DetailView):
    model = Blog
    template_name = 'app_folder/blog_post_detail.html'
    context_object_name = 'blog_post'

# 5. 検索ビュー（ここを大きく修正！）
# クラス(SearchView)から関数(search_view)に変更して、ブログを検索するようにしました
def search_view(request):
    # HTMLの <input name="keyword"> から検索語句を受け取る
    query = request.GET.get('keyword') 
    results = []

    if query:
        # Blogモデルの「タイトル」または「本文」に検索語句が含まれているものを探す
        results = Blog.objects.filter(
            Q(title__icontains=query) | Q(content__icontains=query)
        ).order_by('-created_at') # 新しい順に並べる

    return render(request, 'app_folder/search_results.html', {
        'query': query,
        'results': results,
    })