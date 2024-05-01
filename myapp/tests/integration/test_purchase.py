from django.test import TestCase

from myapp.models import User, Product, Purchase


class PurchaseTestCase(TestCase):
    def test_purchase(self, purchase=None):
        user = User.objects.create_user(username='test', password='pass')
        product = Product.objects.create(name='test', price=100, amount=100)
        self.client.force_login(user)
        data = {'product_id': str(product.pk), "quantity": 5}
        response = self.client.post('/purchase/', data=data)
        self.assertEquals(response.status_code, 302)
        self.assertIsInstance(purchase, Purchase)
        self.assertEquals(purchase.quantity, 5)
        self.assertEquals(purchase.product, product)
        self.assertEquals(purchase.product.amount, 95)
        self.assertEquals(purchase.user.wallet, '9500')