from unittest.mock import patch

from django.core.exceptions import ValidationError
from django.test import TestCase, RequestFactory
from rest_framework.templatetags.rest_framework import data

from myapp.forms import PurchaseForm
from myapp.models import User, Product
from django import forms

class PurchaseFormTestCase(TestCase):

    def __init__(self, methodName: str = ...):
        super().__init__(methodName)
        self.data = None

    def setUp(self):
        self.user = User.objects.create_user(username='test', password='pass')
        self.request = RequestFactory().get('/')
        self.request.user = self.user
        self.product = Product.objects.create(name='test', price=100, amount=100)
        self.date = {'product_id': str(self.product.pk), "quantity": 5}

    def test_purchase_form_init_empty_request(self):
        pf = PurchaseForm()
        self.assertIsNone(pf.request)

    def test_purchase_form_init_not_empty_request(self):
        request = RequestFactory().get('/')
        pf = PurchaseForm(request=request)
        self.assertEquals(pf.request, request)

    def test_clean(self):
        pf = PurchaseForm(self.data, request=self.request)
        pf.is_valid()
        self.assertEquals(pf.clean(), {'quantity': 5})
        self.assertEquals(pf.product, self.product)

    def test_check_product_exist(self):
        data = {'product_id': str(self.product.pk), "quantity": 5}
        pf = PurchaseForm(data, request=self.request)
        self.assertEquals(pf.check_product_exist(), self.product)

    @patch('application.forms.messages')
    def test_check_product_exist_not_exist(self, mock_messages):
        mock_messages.error.return_value = ""
        data = {"quantity": 5}
        pf = PurchaseForm(data, request=self.request)
        with self.assertEquals(forms.ValidationError):
            pf.check_product_exist()

    @patch('application.forms.messages')
    def test_check_product_exist_incorrect_id(self, mock_messages):
        mock_messages.error.return_value = ""
        data = {"product_id": "10000", "quantity": 5}
        pf = PurchaseForm(data, request=self.request)
        with self.assertEquals(forms.ValidationError):
            pf.check_product_exist()