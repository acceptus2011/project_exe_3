from django.contrib.auth.hashers import make_password
from django.core.validators import MinValueValidator
from rest_framework import serializers

from myapp.models import User, Product, Purchase, Return
from django.db.models import Q

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def validate(self, attrs):
        username = attrs.get('username')
        email = attrs.get('email')
        user_exist = Q(username__iexact=username) | Q(email__iexact=email)
        if User.objects.filter(user_exist).count():
            raise serializers.ValidationError('Username or email already exists')
        return attrs

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['description', 'amount', 'name', 'price', 'id', 'picture']

class PurchaseSerializer(serializers.ModelSerializer):
    quantity = serializers.IntegerField(required=True, validators=[MinValueValidator(1)])
    class Meta:
        model = Purchase
        fields = ['id', 'product', 'quantity']

    def validate(self, attrs):
        product = attrs.get('product')
        user = self.context['request'].user
        quantity = attrs.get('quantity')
        if product.amount < quantity:
            raise serializers.ValidationError('Not enough quantity available')
        if user.wallet < product.price * quantity:
            raise serializers.ValidationError('Not enough money')
        return attrs



class ReturnSerializer(serializers.ModelSerializer):
    class Meta:
        model = Return
        fields = ['id', 'purchase']


    def validate(self, attrs):
        user = self.context['request'].user
        purchase = attrs.get('purchase')
        if purchase.user != user:
            raise serializers.ValidationError('You can only return your own purchases')
        if purchase.not_returnable:
            raise serializers.ValidationError('Return time is expired')
        return attrs
