import json

import jsonschema
from django.contrib.auth import authenticate
from django.core.exceptions import ValidationError
from django.http import JsonResponse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_exempt

from xiangqi.models import Token


@method_decorator(csrf_exempt, name="dispatch")
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
            payload = json.loads(request.body.decode())
            jsonschema.validate(payload, self.post_schema)
            token = self.get_token(payload)
            response = JsonResponse({'access_token': token.string}, status=201)
            response.set_cookie(
                'access-token',
                token.string,
                expires=token.expires_on,
                domain='localhost',
                httponly=True,
            )
            return response
        except json.JSONDecodeError:
            return JsonResponse({"error": 'Error parsing request'}, status=400)
        except jsonschema.ValidationError as e:
            return JsonResponse({"error": e.message}, status=400)
        except ValidationError as e:
            return JsonResponse({"error": e.message}, status=401)

    def get_token(self, payload):
        user = authenticate(**payload)
        print(user)
        if user is None:
            raise ValidationError('Authentication failed')
        return Token.objects.create(user)
