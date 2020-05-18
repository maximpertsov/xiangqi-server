from django.conf import settings
from rest_framework_jwt.views import RefreshJSONWebToken, RefreshJSONWebTokenSerializer


class RefreshJSONWebTokenFromCookieSerializer(RefreshJSONWebTokenSerializer):
    def get_fields(self):
        fields = super().get_fields()
        del fields["token"]
        return fields

    def validate(self, attrs):
        attrs.update(
            token=self.context["request"].COOKIES.get(
                settings.JWT_AUTH["JWT_AUTH_COOKIE"]
            )
        )
        return super().validate(attrs)


class RefreshJSONWebTokenFromCookie(RefreshJSONWebToken):
    serializer_class = RefreshJSONWebTokenFromCookieSerializer
