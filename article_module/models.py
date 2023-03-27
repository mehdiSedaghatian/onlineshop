from django.db import models
from jalali_date import date2jalali
from account_module.models import User
from django.contrib.contenttypes.fields import GenericRelation
from star_ratings.models import Rating
from django.utils.translation import gettext_lazy as _


# Create your models here.
class ArticleCategory(models.Model):
    parent = models.ForeignKey('ArticleCategory', null=True, blank=True, on_delete=models.CASCADE,
                               verbose_name='parent of category')
    title = models.CharField(max_length=200, verbose_name='title of category')
    url_title = models.CharField(max_length=200, unique=True, verbose_name='title in url ')
    is_active = models.BooleanField(default=True, verbose_name='active/disable')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'article category'
        verbose_name_plural = 'article categories'


class Article(models.Model):
    title = models.CharField(max_length=300, verbose_name=_('title of article'))
    slug = models.SlugField(max_length=400, db_index=True, allow_unicode=True, verbose_name='title in url')
    image = models.ImageField(upload_to='images/article', verbose_name='image of article')
    short_description = models.TextField(verbose_name=_('short description'))
    text = models.TextField(verbose_name=_('text of article'))
    is_active = models.BooleanField(default=True, verbose_name='active/disable')
    selected_category = models.ManyToManyField(ArticleCategory, verbose_name='categories')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='author', null=True, editable=False)
    create_date = models.DateTimeField(verbose_name='create date', auto_now_add=True, editable=False)
    bar = models.CharField(max_length=100, default=1)
    ratings = GenericRelation(Rating, related_query_name='foos')

    # def __init__(self, *args, **kwargs):
    #     super().__init__(args, kwargs)
    #     self.create_date = None

    def __str__(self):
        return self.title

    def get_jalali_create_date(self):
        return date2jalali(self.create_date)

    def get_jalali_create_time(self):
        return self.create_date.strftime('%H:%M')

    class Meta:
        verbose_name = 'article'
        verbose_name_plural = 'articles'


class ArticleComment(models.Model):
    create_date = models.DateTimeField(auto_now_add=True, verbose_name='create date')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user')
    text = models.TextField(verbose_name='text')
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='article')
    parent = models.ForeignKey('ArticleComment', on_delete=models.CASCADE, verbose_name='parent', null=True, blank=True)

    class Meta:
        verbose_name = 'article comment'
        verbose_name_plural = 'article comments'

    def __str__(self):
        return str(self.user)


class ArticleVisit(models.Model):
    article = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name='article')
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='user', null=True, blank=True)
    ip = models.CharField(max_length=30, verbose_name='user ip')

    def __str__(self):
        return f"{self.article} / {self.id}"

    class Meta:
        verbose_name = 'article visit'
        verbose_name_plural = 'articles visit'
