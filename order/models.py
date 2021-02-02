from django.db import models
from shop.models import Product

from decimal import Decimal

class Order(models.Model):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    address = models.CharField(max_length=250)
    postal_code = models.CharField(max_length=20)
    city = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    paid = models.BooleanField(default=False)

    class Meta:
        ordering = ('-created',)

    def __str__(self):
       return 'Order {}'.format(self.id)

    def get_total_cost(self):
       return sum(item.get_cost() for item in self.items.all())

    def get_total_cost_incl_shipment(self):
        return self.get_total_cost() + Decimal('5.50')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='order_items', on_delete=models.CASCADE)
    player = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
       return '{}'.format(self.id)

    def get_cost(self):
       return self.price * self.quantity

    def get_product_attributes(self):
        player_items = self.items_attribute.all().values()
        attributes_and_quantities = []
        for item in player_items:
            attributes_and_quantities.append([item['player'], item['quantity']])
        return attributes_and_quantities

class AtrributeOfOrderItem(models.Model):
    order_item = models.ForeignKey(OrderItem, related_name='items_attribute', on_delete=models.CASCADE)
    player = models.CharField(max_length=20)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return '{}'.format(self.player)
