from datetime import timedelta

from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.template.defaulttags import now
from django.conf import settings
from pyexpat.errors import messages
from django.contrib import messages

from myapp.models import User, Purchase, Product, Return


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
        except Product.DoesNotExist:
            messages.error(request, "Product does not exist")
            raise forms.ValidationError("Product does not exist")
        quantity = int(cleaned_data.get('quantity'))
        if quantity > product.amount:
            messages.error(request, "Not enough quantity available")
            self.add_error(None, "Not enough quantity available")
        if quantity * product.price > request.user.wallet:
            messages.error(request, "Insufficient funds")
            self.add_error(None, "Insufficient funds")
        self.product = product


class ReturnForm(forms.ModelForm):
    class Meta:
        model = Return
        exclude = ('purchase',)

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request', None)
        super().__init__(*args, **kwargs)
    def clean(self):
        cleaned_data = super().clean()
        request = self.request
        purchase_id = self.data.get('purchase_id')
        try:
            purchase = Purchase.objects.get(pk=purchase_id)
        except Purchase.DoesNotExist:
            messages.error(request, "Purchase does not exist")
            raise forms.ValidationError("Purchase does not exist")
        if (now() - purchase.created_at).seconds > settings.RETURN_ALLOWED_TIME:
            messages.error(request, "Return time has expired")
            self.add_error(None, "Return time has expired")
        self.purchase = purchase