from django.db import models
from django.contrib.auth.models import User
from django_ckeditor_5.fields import CKEditor5Field

# 1. カテゴリ（タグ・ハッシュタグ）
class Category(models.Model):
    name = models.CharField(max_length=50, verbose_name="カテゴリ名")
    image = models.ImageField(upload_to='category_images/', blank=True, null=True, verbose_name='スライド用画像')
    
    # バッジの色設定
    COLOR_CHOICES = [
        ('bg-red-500', '赤（入試・重要）'),
        ('bg-blue-500', '青（就職・将来）'),
        ('bg-green-500', '緑（学問・在学生）'),
        ('bg-yellow-500', '黄（お金・生活）'),
        ('bg-pink-500', 'ピンク（遊び・サークル）'),
        ('bg-gray-500', 'グレー（その他）'),
        ('bg-indigo-500', '紫（コラム・その他）'),
    ]
    color = models.CharField(
        max_length=50, 
        choices=COLOR_CHOICES, 
        default='bg-gray-500',
        verbose_name="バッジの色"
    )
    
    # 表示順（1:遊び, 2:学問... と並べるため）
    order = models.IntegerField(default=0, verbose_name="表示順")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "カテゴリ"
        verbose_name_plural = "カテゴリ"
        ordering = ['order']  # 常にこの順番で表示する
    


# 2. 団体・組織（研究室やサークル）
class Organization(models.Model):
    name = models.CharField(max_length=100, verbose_name="団体名")
    
    # 団体の種類
    TYPE_CHOICES = [
        ('lab', '研究室'),
        ('circle', 'サークル・部活'),
        ('facility', '施設・食堂'),
        ('dept', '学科'),
        ('other', 'その他'),
    ]
    type = models.CharField(max_length=20, choices=TYPE_CHOICES, default='lab', verbose_name="種類")
    
    # 教授名（研究室用）
    professor = models.CharField(max_length=100, blank=True, verbose_name="教授名")
    
    # 説明文
    description = models.TextField(blank=True, verbose_name="紹介文")
    
    # 画像
    image = models.ImageField(upload_to='org_images/', null=True, blank=True, verbose_name="画像")

    def __str__(self):
        return f"[{self.get_type_display()}] {self.name}"

    class Meta:
        verbose_name = "団体・組織"
        verbose_name_plural = "団体・組織"


# 3. ブログ記事
class Blog(models.Model):
    title = models.CharField(max_length=200, verbose_name="タイトル")
    content = CKEditor5Field(config_name='extends', blank=True, null=True, verbose_name="本文")
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="投稿者")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="作成日")
    updated_at = models.DateTimeField(auto_now=True, verbose_name="更新日")
    
    # ★複数選択OKのカテゴリ（タグ）
    categories = models.ManyToManyField(Category, related_name='blogs', verbose_name="カテゴリ")
    
    # ★所属団体（なくてもOK）
    organization = models.ForeignKey(Organization, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="関連団体")

    def __str__(self):
        return self.title

    # ↓↓↓ Blogクラスの中に追加 ↓↓↓
    def save(self, *args, **kwargs):
        if self.content:
            self.content = self.content.replace('&nbsp;', ' ')
        super().save(*args, **kwargs)
    class Meta:
        verbose_name = "ブログ記事"
        verbose_name_plural = "ブログ記事"
        ordering = ['-created_at']

class Comment(models.Model):
    post = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    author = models.CharField('お名前', max_length=50)
    text = models.TextField('コメント内容')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.author} - {self.post.title}"




class SiteRequest(models.Model):
    name = models.CharField('お名前', max_length=50, blank=True, null=True, help_text="匿名でもOKです")
    email = models.EmailField('メールアドレス', blank=True, null=True, help_text="返信が必要な場合は入力してください")
    content = models.TextField('ご要望・お問い合わせ内容')
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField('既読', default=False) # 管理者が読んだかどうかのチェック用

    def __str__(self):
        return f"要望: {self.content[:20]}..."
    