from django.db.models import Count
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render
from django.views import View
from django.views.generic import DetailView
from django.views.generic.list import ListView
from jalali_date import date2jalali, datetime2jalali
from article_module.models import Article, ArticleCategory, ArticleComment, ArticleVisit
from utils.http_service import get_client_ip


# Create your views here.
# class ArticleView(View):
#     def get(self, request):
#         articles = Article.objects.filter(is_active=True)
#         context = {
#             'articles': articles
#         }
#         return render(request, 'article_module/articles_page.html', context)

class ArticleListView(ListView):
    template_name = 'article_module/articles_page.html'
    model = Article
    paginate_by = 5
    ordering = ['-id']

    def get_queryset(self):
        query = super(ArticleListView, self).get_queryset()
        query = query.filter(is_active=True)
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_category__url_title__iexact=category_name)

        return query


class ArticleListStarsView(ListView):
    template_name = 'article_module/articles_page_order_by_stars.html'
    model = Article
    paginate_by = 5

    def get_queryset(self):
        query = super(ArticleListStarsView, self).get_queryset()
        query = query.filter(is_active=True)
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_category__url_title__iexact=category_name)

        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleListStarsView, self).get_context_data()
        context['order_by_stars'] = Article.objects.filter(ratings__isnull=False).order_by('-ratings__average')
        return context


class ArticleListCreateDateView(ListView):
    template_name = 'article_module/article_page_create_date.html'
    model = Article
    paginate_by = 5

    def get_queryset(self):
        query = super(ArticleListCreateDateView, self).get_queryset()
        query = query.filter(is_active=True)
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_category__url_title__iexact=category_name)

        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleListCreateDateView, self).get_context_data()
        context['order_by_crate_date'] = Article.objects.filter(ratings__isnull=False).order_by('-create_date')
        return context


class ArticleListViewsView(ListView):
    template_name = 'article_module/articles_page_views.html'
    model = Article
    paginate_by = 5

    def get_queryset(self):
        query = super(ArticleListViewsView, self).get_queryset()
        query = query.filter(is_active=True)
        category_name = self.kwargs.get('category')
        if category_name is not None:
            query = query.filter(selected_category__url_title__iexact=category_name)

        return query

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super(ArticleListViewsView, self).get_context_data()
        most_visit_articles = Article.objects.filter(is_active=True).annotate(visit_count=Count('articlevisit')).order_by('-visit_count')
        context['most_visit_articles'] = most_visit_articles
        return context


class ArticleDetailView(DetailView):
    template_name = 'article_module/article_detail_page.html'
    model = Article

    def get_queryset(self):
        query = super(ArticleDetailView, self).get_queryset()
        query = query.filter(is_active=True)
        return query

    def get_context_data(self, **kwargs):
        context = super(ArticleDetailView, self).get_context_data()
        article: Article = kwargs.get('object')
        user_ip = get_client_ip(self.request)
        user_id = None
        if self.request.user.is_authenticated:
            user_id = self.request.user.id
        has_been_visited = ArticleVisit.objects.filter(ip__iexact=user_ip, article_id=article.id).exists()
        if not has_been_visited:
            new_visit = ArticleVisit(ip=user_ip, user_id=user_id, article_id=article.id)
            new_visit.save()

        context['comments'] = ArticleComment.objects.filter(article_id=article.id, parent=None).order_by('-create_date').prefetch_related('articlecomment_set')
        context['comments_count'] = ArticleComment.objects.filter(article_id=article.id).count()
        return context


def article_categories_component(request: HttpRequest):
    article_main_categories = ArticleCategory.objects.prefetch_related('articlecategory_set').filter(is_active=True, parent_id=None)
    context = {
        'article_main_categories': article_main_categories
    }
    return render(request, 'article_module/components/article_categories_component.html', context)


def add_article_comment(request: HttpRequest):
    if request.user.is_authenticated:
        article_id = request.GET.get('article_id')
        article_comment = request.GET.get('article_comment')
        parent_id = request.GET.get('parent_id')
        new_comment = ArticleComment(text=article_comment, user_id=request.user.id, article_id=article_id, parent_id=parent_id)
        new_comment.save()
        context = {
            'comments': ArticleComment.objects.filter(article_id=article_id, parent=None).order_by('-create_date').prefetch_related('articlecomment_set'),
            'comments_count': ArticleComment.objects.filter(article_id=article_id).count()
        }
        return render(request, 'article_module/includes/article_comments_partial.html', context)

    return HttpResponse('response')
