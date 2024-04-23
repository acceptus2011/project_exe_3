from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from myapp.api.resources import RegisterApiView

urlpatterns = [
    path("auth/", obtain_auth_token, name='auth_token'),
    path("register/", RegisterApiView.as_view(), name='register')
]