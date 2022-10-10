
from django.shortcuts import render

from boutique.models import Product, ReviewRating


def accueil_view(request):
    # reviews = ReviewRating.objects.filter(product_id=article.id, status=True)
    articles = Product.objects.all().filter(is_available=True).order_by('created_date')

    # Get the reviews
    reviews = None
    for article in articles:
        reviews = ReviewRating.objects.filter(product_id=article.id, status=True)

    context = {
        'articles': articles,
        'reviews': reviews,
    }
    return render(request, 'accueil.html', context)