from django.views.generic import ListView
from django.shortcuts import render, get_object_or_404

from shop.models import Product
from cart.forms import CartAddProductForm

class ProductListView(ListView):
    queryset = Product.objects.filter(available=True)
    template_name = "product/list.html"

    def get_queryset(self):
        self.qs = super(ProductListView, self).get_queryset().filter(available=True)
        return self.qs

    def get_context_data(self):
        context = super(ProductListView, self).get_context_data()
        context['products'] = self.qs
        return context


def product_detail(request, id, slug):
    product = get_object_or_404(Product, id=id, slug=slug, available=True)
    cart_product_form = CartAddProductForm(product)
    return render(request, 'product/detail.html', {'product': product, 'cart_product_form': cart_product_form})

