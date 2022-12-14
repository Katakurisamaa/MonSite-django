from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    path('admin/', include('admin_honeypot.urls', namespace='admin_honeypot')),
    path('securityrelooking/', admin.site.urls),
    path('', views.accueil_view, name="accueil"),
    path('boutique/',include('boutique.urls')),
    path('cart/',include('cart.urls')),
    path('comptes/', include('comptes.urls')),
    # commandes
    path('commandes/', include('commandes.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)