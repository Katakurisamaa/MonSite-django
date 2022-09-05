from django.http import HttpResponse
from itertools import product
from django.shortcuts import get_object_or_404, render
from category.models import Category
from cart.models import CartItem
from .models import Product
from cart.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q


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
        paginator = Paginator(articles,6)
        page = request.GET.get('page')
        page_article = paginator.get_page(page)
        article_count = articles.count()
    else:
        articles = Product.objects.all().filter(is_available=True).order_by('id')
        paginator = Paginator(articles,9)
        page = request.GET.get('page')
        page_article = paginator.get_page(page)
        article_count = articles.count()

    context = {
        'articles': page_article,
        'article_count': article_count,
    }
    return render(request, 'boutique/article.html', context)

def details_view(request, category_slug, slug):
    try:
        article = Product.objects.get(category__slug=category_slug, slug=slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=article).exists()
    except Exception as e:
        raise e
    context = {
        'article':article,
        'in_cart': in_cart,
        }
    return render(request, 'boutique/details.html', context)

def search_view(request):
    if 'keyword' in request.GET:
        keyword = request.GET['keyword']
        if keyword:
            articles = Product.objects.order_by('created_date').filter(Q(description__icontains=keyword) | Q(product_name__icontains=keyword))
            article_count = articles.count() 
    context = {
        'articles':articles,
        'article_count':article_count,
    }
    return render(request,'boutique/article.html',context)