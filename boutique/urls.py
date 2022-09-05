from django.urls import path
from . import views

urlpatterns = [
    path('', views.boutique_view, name="boutique"),
    path('category/<slug:category_slug>/', views.boutique_view, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:slug>/', views.details_view, name="details"),
    path('search/', views.search_view, name="search"),
]