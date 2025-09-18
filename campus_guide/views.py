# campus_guide/views.py

from django.shortcuts import render
from django.views import View, generic
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from .models import University, Blog


from django.http import HttpResponse, Http404
from django.conf import settings
import os


class SampleView(View):
    def get(self, request, *args, **kwargs):
        university_list = University.objects.all().order_by('id')
        
        paginator = Paginator(university_list, 4)
        page_number = request.GET.get('page')
        try:
            page_obj = paginator.page(page_number)
        except PageNotAnInteger:
            page_obj = paginator.page(1)
        except EmptyPage:
            page_obj = paginator.page(paginator.num_pages)
        
        context = {
            'page_obj': page_obj,
        }
        return render(request, 'app_folder/page01.html', context=context)

top_page = SampleView.as_view()


class SearchView(View):
    def get(self, request, *args, **kwargs):
        query = request.GET.get('input_data')
        if query:
            results = University.objects.filter(name__icontains=query)
        else:
            results = []
        
        context = {
            'results': results,
            'query': query,
        }
        return render(request, 'app_folder/page02.html', context=context)

search_view = SearchView.as_view()


class UniversityDetailView(generic.DetailView):
    model = University
    template_name = 'app_folder/detail_base.html'
    context_object_name = 'university'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['blogs'] = Blog.objects.filter(university=self.object).order_by('-created_at')
        return context

detail_page = UniversityDetailView.as_view()


class BlogPostDetailView(generic.DetailView):
    model = Blog
    template_name = 'app_folder/blog_post_detail.html'
    context_object_name = 'blog_post'

blog_post_detail_view = BlogPostDetailView.as_view()



def serve_media_debug(request, path):
    """
    本番環境でのメディアファイルアクセスをデバッグするためのテスト用ビュー。
    ファイルパスを直接指定して、ファイルが存在し、読み取り可能かを確認します。
    """
    # MEDIA_ROOT とリクエストされたパスを結合して、ファイルの絶対パスを作成
    file_path = os.path.join(settings.MEDIA_ROOT, path)

    # ファイルがその場所に物理的に存在するかを確認
    if os.path.exists(file_path):
        # ファイルが存在すれば、それを読み込んでブラウザに返す
        with open(file_path, 'rb') as f:
            # content_typeはファイルの種類に合わせて変更が必要な場合がある
            return HttpResponse(f.read(), content_type="image/jpeg")
    
    # ファイルが存在しなければ404エラーを発生させる
    raise Http404("Debug: File not found at " + file_path)