from django.urls import path, include
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from myapp.api.resources import RegisterApiView, ProductModelViewSet, PurchaseModelViewSet, ReturnModelViewSet

router = routers.DefaultRouter()
router.register(r'products', ProductModelViewSet)
router.register(r'purchases', PurchaseModelViewSet)
router.register(r'returns', ReturnModelViewSet)


urlpatterns = [
    path("auth/", obtain_auth_token, name='auth_token'),
    path("register/", RegisterApiView.as_view(), name='register'),
    path("", include(router.urls)),
]