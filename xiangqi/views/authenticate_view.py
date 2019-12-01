import json

import jsonschema
from django.conf import settings
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils import timezone
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import ensure_csrf_cookie

from xiangqi.models import AccessToken, RefreshToken, Token, User

JWT_COOKIE = "access_token"
REFRESH_COOKIE = "refresh_token"


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
            return JsonResponse({"error": "Authentication failed"}, status=401)

        tokens = {
            JWT_COOKIE: create_access_token(user),
            REFRESH_COOKIE: create_refresh_token(user),
        }

        response = JsonResponse({}, status=201)
        for cookie, token in tokens.items():
            response.set_cookie(
                cookie, token.token, domain=settings.CLIENT_DOMAIN, httponly=True
            )
        return response


# TODO: break this up into a login and authenticate view?
@method_decorator(ensure_csrf_cookie, name="dispatch")
class AuthenticateView(View):
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
            user = self.get_user_from_cookie(request)
            if user is None:
                user = self.get_user_from_payload(request)
                if user is None:
                    raise ValidationError("Authentication failed")

            token = self.get_new_token(user)

            response = JsonResponse({"access_token": token.string}, status=201)
            response.set_cookie(
                JWT_COOKIE,
                token.string,
                expires=token.expires_on,
                domain=settings.CLIENT_DOMAIN,
                httponly=True,
            )
            return response
        except json.JSONDecodeError:
            return JsonResponse({"error": "Error parsing request"}, status=400)
        except jsonschema.ValidationError as e:
            return JsonResponse({"error": e.message}, status=400)
        except ValidationError as e:
            return JsonResponse({"error": e.message}, status=401)

    def get_user_from_cookie(self, request):
        try:
            string = request.COOKIES[JWT_COOKIE]
            token = self.get_and_expire_active_token(string)
            return token.get_user()
        except (KeyError, Token.DoesNotExist, User.DoesNotExist):
            return

    def get_user_from_payload(self, request):
        payload = json.loads(request.body.decode())
        jsonschema.validate(payload, self.post_schema)
        return authenticate(**payload)

    def get_and_expire_active_token(self, string):
        token = Token.objects.get(string=string)
        if token.expires_on > timezone.now():
            return token
        raise ValidationError("Expired token")

    def get_new_token(self, user):
        return Token.objects.create(user)
