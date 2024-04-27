from django.conf import settings
from django.template.defaulttags import now
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import AuthenticationFailed


class TokenExpiredAuthentication(TokenAuthentication):
    def authenticate(self, request):
        try:
            user, token = super().authenticate(request)
        except TypeError:
            return
        if (now() - token.created).second > settings.TOKEN_EXPIRE_SECONDS:
            token.delete()
            raise AuthenticationFailed("Token expired. Please take new one")
        return user, token