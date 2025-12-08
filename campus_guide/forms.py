from django import forms
# もし Comment モデルを作っていない場合は、下の行の Comment を消して SiteRequest だけにしてください
from .models import Comment, SiteRequest

# 1. コメント機能用のフォーム
class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['author', 'text']
        widgets = {
            'author': forms.TextInput(attrs={
                'class': 'w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'お名前（ニックネーム可）'
            }),
            'text': forms.Textarea(attrs={
                'class': 'w-full p-2 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'rows': 4,
                'placeholder': '記事の感想を書いてね！'
            }),
        }

# 2. 要望・お問い合わせ機能用のフォーム
class SiteRequestForm(forms.ModelForm):
    class Meta:
        model = SiteRequest
        fields = ['name', 'email', 'content']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'お名前（匿名可）'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'placeholder': 'example@email.com（任意）'
            }),
            'content': forms.Textarea(attrs={
                'class': 'w-full p-3 border rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-500',
                'rows': 6,
                'placeholder': 'サイトへのご要望、バグ報告、感想などをお書きください。'
            }),
        }