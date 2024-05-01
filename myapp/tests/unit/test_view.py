from django.test import TestCase, RequestFactory
from rest_framework.templatetags.rest_framework import data

from myapp.forms import PurchaseForm
from myapp.models import User, Product, Purchase
from myapp.views import PurchaseView


class PurchaseViewTestCase(TestCase):
    def test_get_form_kwargs(self):
        request = RequestFactory().get('/')
        view = PurchaseView()
        view.setup(request)
        context = view.get_form_kwargs()
        self.assertIn('request', context)

    def test_form_valid(self):
        user = User.objects.create_user(username='test', password='pass')
        request = RequestFactory().post('/')
        request.user = user
        product = Product.objects.create(name='test', price=100, amount=100)
        date = {'product_id': str(product.pk), "quantity": 5}
        pf = PurchaseForm(data, request=request)
        pf.is_valid()
        view = PurchaseView()
        view.setup(request)
        response = view.form_valid(form=pf)
        self.assertEquals(response.status_code, 302)
        purchase = view.object
        self.assertIsInstance(purchase, Purchase)
        self.assertEquals(purchase.quantity, 5)
        self.assertEquals(purchase.product, product)
        self.assertEquals(purchase.product.amount, 95)
        self.assertEquals(request.user.wallet, '9500')