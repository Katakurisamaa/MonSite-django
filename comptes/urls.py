from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_view, name="register"),
    path('login/', views.login_view, name="login"),
    path('logout/', views.logout_view, name="logout"),
    path('dashboard/', views.dashboard_view, name="dashboard"),
    path('', views.dashboard_view, name="dashboard"),

    path('activate/<uidb64>/<token>/', views.activate_view, name="activate"),
    path('forgotPassword/', views.forgotPassword_view, name="forgotPassword"),
    path('resetPassword/', views.resetPassword_view, name="resetPassword"),
    path('resetpassword_validate/<uidb64>/<token>/', views.resetpassword_validate_view, name="resetpassword_validate"),

    path('resetPassword/', views.resetPassword_view, name="resetPassword"),
    path('my_orders/', views.my_orders_view, name="my_orders"),
    path('edit_profile/', views.edit_profile_view, name="edit_profile"),
    path('change_password/', views.change_password_view, name="change_password"),
    path('order_detail/<int:order_id>/', views.order_detail_view, name="order_detail"),
]