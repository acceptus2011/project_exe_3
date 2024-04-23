from django.contrib.auth.hashers import make_password
from rest_framework import serializers

from myapp.models import User
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
        password = validated_data.pop('password', None)
        password = make_password(password)
        return User.objects.create_user(password=password, **validated_data)