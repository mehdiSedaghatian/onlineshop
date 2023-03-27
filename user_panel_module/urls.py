from django.urls import path

from . import views

urlpatterns = [
    path('', views.UserPanelDashboardPage.as_view(), name='user_panel_dashboard'),
    path('edit-profile/', views.EditUserProfilePage.as_view(), name='edit_profile_page'),
    path('change-password/', views.ChangePasswordPage.as_view(), name='change_password_page'),
    path('user-basket/', views.user_basket, name='user_basket_page'),
    path('my-shopping', views.MySopping.as_view(), name='user_shopping_page'),
    path('my-shopping-detail/<order_id>', views.my_shopping_detail, name='my_shopping_detail'),
    path('remove-order-detail', views.user_remove_order, name='remove_order_detail_ajax'),
    path('change-order-detail-count', views.change_order_detail_count, name='change_order_detail_count'),
]
