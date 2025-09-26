# campus_guide/views.py

from django.shortcuts import render
from django.views import View, generic
from .models import University, Campus, Blog
from django.db.models import Q

# 1. トップページ：大学一覧を表示するビュー
class TopPage(generic.ListView):
    model = University
    template_name = 'app_folder/university_list.html'  # ← 修正
    context_object_name = 'universities'
    paginate_by = 6

# 2. 大学詳細ページ：キャンパス一覧を表示するビュー
class UniversityDetailView(generic.DetailView):
    model = University
    template_name = 'app_folder/university_detail.html' # ← 修正
    context_object_name = 'university'

# 3. キャンパス詳細ページ：ブログ一覧を表示するビュー
class CampusDetailView(generic.DetailView):
    model = Campus
    template_name = 'app_folder/campus_detail.html' # ← 修正
    context_object_name = 'campus'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = self.object.blogs.all().order_by('-created_at')
        return context

# 4. ブログ詳細ページ
class BlogPostDetailView(generic.DetailView):
    model = Blog
    template_name = 'app_folder/blog_post_detail.html' # ← 修正
    context_object_name = 'blog_post'

# 5. 検索ビュー
class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = self.request.GET.get('input_data')
        if query:
            results = Campus.objects.select_related('university').filter(
                Q(name__icontains=query) | Q(university__name__icontains=query)
            )
        else:
            results = Campus.objects.none()
        # ↓ 戻り値のテンプレート名も修正
        return render(request, 'app_folder/search_results.html', {'results': results, 'query': query})