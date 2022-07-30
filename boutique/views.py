from django.shortcuts import get_object_or_404, render

from category.models import Category

from .models import Product



# Create your views here.
# def boutique_view(request):
#     articles = Product.objects.all().order_by('-created_date')
#     context={'articles': articles}
#     return render(request, 'boutique/article.html', context)

def boutique_view(request, category_slug=None):
    categories = None
    articles = None

    if category_slug != None:
        categories = get_object_or_404(Category, slug=category_slug)
        articles = Product.objects.filter(category=categories, is_available=True)
        article_count = articles.count()
    else:
        articles = Product.objects.all().filter(is_available=True).order_by('id')
        article_count = articles.count()

    context = {
        'articles': articles,
        'article_count': article_count,
    }
    return render(request, 'boutique/article.html', context)

def details_view(request, category_slug, slug):
    try:
        article = Product.objects.get(category__slug=category_slug, slug=slug)
    except Exception as e:
        raise e
    context = {'article':article}
    return render(request, 'boutique/details.html', context)