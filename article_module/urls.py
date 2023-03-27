from . import views
from django.urls import path

urlpatterns = [
    path('', views.ArticleListView.as_view(), name='article_list'),
    path('order-by-stars', views.ArticleListStarsView.as_view(), name='article_list_stars'),
    path('order-by-create-time', views.ArticleListCreateDateView.as_view(), name='article_list_create_date'),
    path('order-by-number-of-views', views.ArticleListViewsView.as_view(), name='article_list_views'),
    path('cat/<str:category>', views.ArticleListView.as_view(), name='article_by_category_list'),
    path('<pk>/', views.ArticleDetailView.as_view(), name='article_detail'),
    path('add-article-comment', views.add_article_comment, name='add_article_comment')
]
