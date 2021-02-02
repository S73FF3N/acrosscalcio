from django import forms

from shop.models import Product
from allstar_teams.models import Player, AllstarTeam

from dal import autocomplete

PRODUCT_QUANTITY_CHOICES = [(i, str(i)) for i in range(1, 6)]

class CartAddProductForm(forms.ModelForm):

    quantity = forms.TypedChoiceField(choices=PRODUCT_QUANTITY_CHOICES, coerce=int)
    update = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput)

    def __init__(self, product, *args, **kwargs):
        super(CartAddProductForm, self).__init__(*args, **kwargs)
        self.fields['team'] = forms.ModelChoiceField(queryset=AllstarTeam.objects.filter(available=True), widget=autocomplete.ModelSelect2(url='cart:allstarteam-autocomplete'))
        self.fields['player_available'] = forms.ModelChoiceField(queryset=Player.objects.filter(products_available=product, available=True), widget=autocomplete.ModelSelect2(url='cart:player-autocomplete', forward=['team']))
        self.fields['team'].label = "Team"
        self.fields['player_available'].label = "Player"
        self.fields['team'].required = False
        self.fields['player_available'].required = True
        if len(Player.objects.filter(products_available=product)) <= 1:
            self.fields['team'].widget = forms.HiddenInput()
            self.fields['player_available'].widget = forms.HiddenInput()
            self.fields['team'].initial = AllstarTeam.objects.get(name='None')
            self.fields['player_available'].initial = Player.objects.get(name='None')

    class Meta:
        model = Product
        fields = []