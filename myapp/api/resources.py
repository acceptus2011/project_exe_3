from django.db import transaction
from django.db.migrations import serializer
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response

from myapp.api.serializers import RegisterSerializer, ProductSerializer, PurchaseSerializer, ReturnSerializer
from myapp.models import User, Product, Purchase, Return
from myapp.api.permissions import IsAdminOrReadOnly, IsAdminReturnActions
from django.db.models import Q

class RegisterApiView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []
    queryset = User.objects.all()

class ProductModelViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    http_method_names = ['get', 'post', 'patch']
    permission_classes = [IsAdminOrReadOnly]

class PurchaseModelViewSet(viewsets.ModelViewSet):
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer
    http_method_names = ['get', 'post']

    def get_queryset(self):
        return Purchase.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        product = serializer.validated_data['product']
        quantity = serializer.validated_data['quantity']
        user = self.request.user
        product.amount -= quantity
        user.wallet -= product.price * quantity
        with transaction.atomic():
            product.save()
            user.save()
            serializer.save(user=self.request.user)

class ReturnModelViewSet(viewsets.ModelViewSet):
    queryset = Return.objects.all()
    serializer_class = ReturnSerializer
    http_method_names = ['get', 'post']
    permission_classes = [IsAdminReturnActions]

    def get_queryset(self):
        query = Q()
        if not self.request.user.is_superuser:
            query |= Q(purchase__user=self.request.user)
        return Return.objects.filter(query)

    @action(methods=['post'], detail=True)
    def approve(self, request, pk=None):
        ret = self.get_object()
        purchase = ret.purchase
        user = purchase.user
        product = purchase.product
        quantity = purchase.quantity
        price = product.price
        user.wallet += quantity * price
        product.amount += quantity
        with transaction.atomic():
            user.save()
            product.save()
            purchase.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
    @action(methods=['post'], detail=True)
    def decline(self, request, pk=None):
        ret = self.get_object()
        ret.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)