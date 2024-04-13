from django import forms
from django.contrib.auth.forms import UserCreationForm
from pyexpat.errors import messages

from myapp.models import User, Purchase, Product


class RegisterForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username',)



class PurchaseForm(forms.ModelForm):
    class Meta:
        model = Purchase
        fields = ('quantity',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        cleaned_data = super().clean()
        request = self.request
        product_id = self.data.get('product_id')
        product = Product.objects.get(pk=product_id)
        try:
            product = Product.objects.get(pk=product_id)
        except product.DoesNotExist:
            messages.error(request, "Product does not exist")
            raise forms.ValidationError("Product does not exist")
        quantity = cleaned_data.get('quantity')
        if quantity > product.quantity:
            messages.error(request, "Not enough quantity available")
            self.add_error( None, "Not enough quantity available")