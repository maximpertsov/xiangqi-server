from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.views import View

from xiangqi.models import AccessToken, RefreshToken
from xiangqi.views.payload_schema_mixin import PayloadSchemaMixin

ACCESS_TOKEN_KEY = "access_token"
REFRESH_TOKEN_KEY = "refresh_token"


class AuthenticationFailedResponse(JsonResponse):
    def __init__(self):
        super().__init__({"error": "Authentication failed"}, status=401)


def create_access_token(user):
    # TODO: invalidate active tokens?
    return AccessToken.objects.create(user)


def create_refresh_token(user):
    # TODO: invalidate active tokens?
    return RefreshToken.objects.create(user)


class LoginView(PayloadSchemaMixin, View):
    http_method_names = ["post"]

    @property
    def payload_schema(self):
        return {
            "properties": {
                "username": {"type": "string"},
                "password": {"type": "string"},
            },
            "required": ["username", "password"],
            "additionalProperties": False,
        }

    def post(self, request):
        try:
            user = authenticate(**self.payload)
        except ValidationError as e:
            return JsonResponse({"error": e.message}, status=400)

        if user is None:
            return AuthenticationFailedResponse()

        tokens = {
            ACCESS_TOKEN_KEY: create_access_token(user).token,
            REFRESH_TOKEN_KEY: create_refresh_token(user).token,
        }

        response = JsonResponse(tokens, status=201)
        for cookie, token in tokens.items():
            response.set_cookie(
                cookie, token, domain=settings.CLIENT_DOMAIN, httponly=True
            )
        return response


class AuthenticateView(View):
    http_method_names = ["post"]

    def post(self, request):
        try:
            access_token = request.COOKIES[ACCESS_TOKEN_KEY]
            refresh_token = request.COOKIES[REFRESH_TOKEN_KEY]
            user = AccessToken.objects.get(token=access_token).user
            if user is None:
                return AuthenticationFailedResponse()
        except (AccessToken.DoesNotExist, KeyError):
            return AuthenticationFailedResponse()

        tokens = {ACCESS_TOKEN_KEY: access_token, REFRESH_TOKEN_KEY: refresh_token}
        return JsonResponse(tokens, status=201)
