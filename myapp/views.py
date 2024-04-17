from django.contrib.auth import login
from django.db import transaction
from django.http import request, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import TemplateView, CreateView, ListView, DeleteView
from django.contrib import messages

from myapp.forms import RegisterForm, PurchaseForm, ReturnForm
from myapp.models import Product, Purchase, Return


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

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse_lazy('index'))


class ProfileView(ListView):
    template_name = 'profile.html'

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)


class ReturnCreateView(CreateView):
    form_class = ReturnForm
    success_url = reverse_lazy('profile')

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(selfself, form):
        ret = form.save(commit=False)
        ret.purchase = form.purchase
        ret.save()
        return super().form_valid(form=form)

    def form_invalid(self, form):
        return HttpResponseRedirect(reverse_lazy('profile'))


class ReturnApproveView(DeleteView):
    queryset = Return.objects.all()


class ReturnDeclineView(DeleteView):
    queryset = Return.objects.all()


class ProductCreateView(CreateView):
    model = Product
    fields = '__all__'
    template_name = 'create_product.html'
    success_url = reverse_lazy('index')


class ReturnListView(ListView):
    queryset = Return.objects.all()
    template_name = 'returns_list.html'
