from django.urls import path
from . import views

urlpatterns = [
    path('place_order/', views.place_order_view, name="place_order"),
    path('payments/', views.payments_view, name="payments"),
    path('order_complete/', views.order_complete_view, name="order_complete"),
    path('test/', views.test_view, name="test"),
]