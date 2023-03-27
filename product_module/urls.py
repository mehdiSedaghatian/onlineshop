from . import views
from django.urls import path

urlpatterns = [
    # path('', views.search, name='search'),
    path('', views.ProductListView.as_view(), name='product_list'),
    path('cat/<cat>', views.ProductListView.as_view(), name='product_categories_list'),
    path('brand/<brand>', views.ProductListView.as_view(), name='product_brand_list'),
    path('product-favorite', views.AddProductFavorite.as_view(), name='product-favorite'),
    path('<slug:slug>', views.ProductDetailView.as_view(), name='product-detail'),

]
