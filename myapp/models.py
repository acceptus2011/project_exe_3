from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    wallet = models.PositiveIntegerField(default=10000)


class Product(models.Model):
    objects = None
    description = models.TextField()
    name = models.TextField()
    price = models.IntegerField()
    picture = models.ImageField(upload_to='pictures/')
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.name}, price - {self.price}, amount - {self.amount}"


class Purchase(models.Model):
    DoesNotExist = None
    objects = None
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


class Return(models.Model):
    objects = None
    purchase = models.OneToOneField(Purchase, on_delete=models.CASCADE)
# Create your models here.
