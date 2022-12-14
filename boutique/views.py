from django.contrib import messages
from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from commandes.models import OrderProduct
from django.shortcuts import get_object_or_404, render, redirect
from boutique.forms import ReviewForm
from category.models import Category
from cart.models import Cart, CartItem
from .models import Product, ProductGallery, ReviewRating
from cart.views import _cart_id
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q


# Create your views here.
# def boutique_view(request):
#     articles = Product.objects.all().order_by('-created_date')
#     context={'articles': articles}
#     return render(request, 'boutique/article.html', context)

def boutique_view(request, category_slug=None, reviews=None):
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

    for article in articles.order_by('-created_date'):
        reviews = ReviewRating.objects.filter(product_id=article.id, status=True)
    context = {
        'articles': page_article,
        'article_count': article_count,
        'reviews':reviews,
    }
    return render(request, 'boutique/article.html', context)

def details_view(request, category_slug, slug):
    try:
        article = Product.objects.get(category__slug=category_slug, slug=slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=article).exists()
    except Exception as e:
        raise e
    if request.user.is_authenticated:
        try:
            orderproduct = OrderProduct.objects.filter(user=request.user, product_id=article.id).exists()
        except OrderProduct.DoesNotExist:
            orderproduct = None
    else:
        orderproduct = None

    # Get the reviews
    reviews = ReviewRating.objects.filter(product_id=article.id, status=True)

    # Get the product gallery
    product_gallery = ProductGallery.objects.filter(product_id=article.id)

    context = {
        'article':article,
        'orderproduct': orderproduct,
        'in_cart': in_cart,
        'reviews': reviews,
        'product_gallery':product_gallery,
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


def ajouter_view(request, total=0, quantity=0, cart_items=None, cart=None):
    try:
        tax = 0
        grand_total = 0
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)
        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            
            quantity += cart_item.quantity
        tax = (2 * total)/100
        grand_total = total + tax
    except ObjectDoesNotExist:
        pass #just ignore

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax'       : tax,
        'grand_total': grand_total,
    }
    return render(request, 'boutique/details.html', context)

def submit_review_view(request, product_id):
    url = request.META.get('HTTP_REFERER')
    if request.method == 'POST':
        try:
            reviews = ReviewRating.objects.get(user__id=request.user.id, product__id=product_id)
            form = ReviewForm(request.POST, instance=reviews)
            form.save()
            messages.success(request, 'Merci! Votre avis a ??t?? mis ?? jour.')
            return redirect(url)
        except ReviewRating.DoesNotExist:
            form = ReviewForm(request.POST)
            if form.is_valid():
                data = ReviewRating()
                data.subject = form.cleaned_data['subject']
                data.rating = form.cleaned_data['rating']
                data.review = form.cleaned_data['review']
                data.ip = request.META.get('REMOTE_ADDR')
                data.product_id = product_id
                data.user_id = request.user.id
                data.save()
                messages.success(request, 'Merci! Votre avis a ??t?? soumis.')
                return redirect(url)