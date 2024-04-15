from django.contrib.auth import login
from django.db import transaction
from django.http import request
from django.shortcuts import render
from django.views.generic import TemplateView, CreateView, ListView
from django.contrib import messages

from myapp.forms import RegisterForm, PurchaseForm
from myapp.models import Product, Purchase


# Create your views here.
class ProductListView(ListView):
    template_name = 'index.html'
    queryset = Product.objects.all()
    extra_context = {"form": PurchaseForm}


class RegisterView(CreateView):
    template_name = 'register.html'
    form_class = RegisterForm
    success_url = '/'

    def form_valid(self, form):
        result = super().form_valid(form=form)
        login(self.request, self.object)
        return result


class PurchaseView(CreateView):
    queryset = Purchase.objects.all()
    form_class = PurchaseForm
    success_url = '/'

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        purchase = form.save(commit=False)
        user = self.request.user
        product = form.product
        purchase.user = user
        purchase.product = product
        product.amount -= purchase.quantity
        user.wallet -= purchase.quantity * product.price
        with transaction.atomic():
            product.save()
            purchase.save()
            user.save()
            return super().form_valid(form=form)