from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.views.decorators.csrf import ensure_csrf_cookie


def csrf(request):
    return JsonResponse({'csrf_token': get_token(request)})


@ensure_csrf_cookie
def ping(request):
    return JsonResponse({'result': 'ok'})
