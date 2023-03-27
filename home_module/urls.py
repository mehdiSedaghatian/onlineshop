from django.urls import path
from unicodedata import name

from . import views
urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('search-products/', views.SearchProductsView.as_view(), name='search-products'),
    path('about-us/', views.AboutView.as_view(), name='about_page'),
    path('not-yet-completed/', views.Page404.as_view(), name='not_yet_completed')
]