import json

import jsonschema
from django.conf import settings
from django.contrib.auth import authenticate
from django.http import JsonResponse
from django.views import View

from xiangqi.models import AccessToken, RefreshToken

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


class LoginView(View):
    http_method_names = ["post"]

    @property
    def post_schema(self):
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
            payload = json.loads(request.body.decode())
            jsonschema.validate(payload, self.post_schema)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error parsing request"}, status=400)
        except jsonschema.ValidationError as e:
            return JsonResponse({"error": e.message}, status=400)

        user = authenticate(**payload)
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

    @property
    def post_schema(self):
        # TODO: disallow additional properties
        return {"properties": {}, "required": [], "additionalProperties": True}

    def post(self, request):
        try:
            payload = json.loads(request.body.decode())
            jsonschema.validate(payload, self.post_schema)
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error parsing request"}, status=400)
        except jsonschema.ValidationError as e:
            return JsonResponse({"error": e.message}, status=400)

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
