from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.accueil_view, name="accueil"),
    path('boutique/',include('boutique.urls')),
    path('cart/',include('cart.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
