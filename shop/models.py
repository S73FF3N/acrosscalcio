from django.db import models
from django.urls import reverse

class Product(models.Model):

    name = models.CharField(max_length=100, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    image = models.ImageField(blank=True, upload_to='products')
    description = models.TextField(blank=True)

    available = models.BooleanField(default=True)
    created = models.DateField(auto_now_add=True)
    updated = models.DateField(auto_now=True)

    class Meta:
        index_together = (('id'), ('slug'),)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('shop:product_detail', args=[self.id, self.slug])