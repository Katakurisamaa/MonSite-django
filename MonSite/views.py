
from django.shortcuts import render


def accueil_view(request):
    return render(request, 'accueil.html')