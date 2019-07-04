from django.http import JsonResponse
from django.middleware.csrf import get_token


def csrf(request):
    return JsonResponse({'csrf_token': get_token(request)})


def ping(request):
    return JsonResponse({'result': 'ok'})
