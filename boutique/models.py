from django.db import models
from category.models import Category
from django.urls import reverse

# Create your models here.

class Product(models.Model):
    product_name    = models.CharField(max_length=200, unique=True)
    slug            = models.SlugField(max_length=200, unique=True)
    description     = models.TextField(max_length=500, blank=True)
    price           = models.FloatField(default=0.0)
    images          = models.ImageField(upload_to='boutique')
    stock           = models.IntegerField(default=0)
    is_available    = models.BooleanField(default=True)
    category        = models.ForeignKey(Category, on_delete=models.CASCADE)
    created_date    = models.DateTimeField(auto_now_add=True)
    modified_date   = models.DateTimeField(auto_now=True)

    def get_url(self):
        return reverse('details', args=[self.category.slug, self.slug])
        
    def __str__(self):
        return self.product_name

    class Meta:
        verbose_name = 'Boutique'
        verbose_name_plural = 'articles'
