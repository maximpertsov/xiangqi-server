from django.conf import settings
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView


class TokenCookieObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        for cookie, token in response.data.items():
            response.set_cookie(
                cookie, token, domain=settings.CLIENT_DOMAIN, httponly=True
            )
        return response


class TokenCookieRefreshSerializer(TokenRefreshSerializer):
    def get_fields(self):
        fields = super().get_fields()
        del fields["refresh"]
        return fields

    def validate(self, attrs):
        attrs.update(refresh=self.context["request"].COOKIES["refresh"])
        return super().validate(attrs)


class TokenCookieRefreshView(TokenRefreshView):
    serializer_class = TokenCookieRefreshSerializer

    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        for cookie, token in response.data.items():
            response.set_cookie(
                cookie, token, domain=settings.CLIENT_DOMAIN, httponly=True
            )
        return response
