from django.urls import path
from . import views

urlpatterns = [
    path('', views.boutique_view, name="boutique"),
    path('<slug:category_slug>/', views.boutique_view, name='products_by_category'),
    path('<slug:category_slug>/<slug:slug>/', views.details_view, name="details")
]