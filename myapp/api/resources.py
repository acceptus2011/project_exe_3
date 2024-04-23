from rest_framework.generics import CreateAPIView

from myapp.api.serializers import RegisterSerializer
from myapp.models import User


class RegisterApiView(CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = []
    queryset = User.objects.all()