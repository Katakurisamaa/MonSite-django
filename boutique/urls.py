from django.urls import path
from . import views

urlpatterns = [
    path('', views.boutique_view, name="boutique"),
    path('category/<slug:category_slug>/', views.boutique_view, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:slug>/', views.details_view, name="details"),
    path('category/<slug:category_slug>/<slug:slug>/<int:product_id>', views.ajouter_view, name="ajouter"),
    path('search/', views.search_view, name="search"),
    path('submit_review/<int:product_id>/', views.submit_review_view, name="submit_review"),
]