from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.views.decorators.http import require_POST
from django.contrib import messages

from allstar_teams.models import AllstarTeam, Player
from shop.models import Product
from .cart import Cart
from .forms import CartAddProductForm

from dal import autocomplete

@require_POST
def cart_add(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    form = CartAddProductForm(product, request.POST)

    if form.is_valid():
        cd = form.cleaned_data
        cart.add(product=product, quantity=cd['quantity'], update_quantity=cd['update'], player_available=cd['player_available'].name)
        return redirect('cart:cart_detail')
    else:
        messages.error(request, "Something went wrong. Please try again.")
        return HttpResponseRedirect(product.get_absolute_url())

def cart_add_no_form(request, product_id, player_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    player = get_object_or_404(Player, id=player_id)

    cart.add(product=product, quantity=1, player_available=player.name)
    return redirect('cart:cart_detail')

def cart_remove(request, product_id):
    cart = Cart(request)
    product = get_object_or_404(Product, id=product_id)
    cart.remove(product)
    return redirect('cart:cart_detail')

def cart_detail(request):
    cart = Cart(request)
    return render(request, 'cart/detail.html', {'cart': cart})

class AllstarTeamAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = AllstarTeam.objects.filter(available=True)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs

class PlayerAutocomplete(autocomplete.Select2QuerySetView):
    def get_queryset(self):
        qs = Player.objects.filter(available=True)
        team = self.forwarded.get('team', None)

        if team:
            qs = qs.filter(team=team)

        if self.q:
            qs = qs.filter(name__istartswith=self.q)

        return qs