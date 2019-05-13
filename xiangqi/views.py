import json
import os

from django.conf import settings
from django.http import JsonResponse


def load_fixture(fixture):
    fixture_path = os.path.join(settings.BASE_DIR, 'xiangqi/fixtures', fixture)
    with open(fixture_path) as f:
        return json.load(f)


def allow_cross_origin(f):
    def wrapped(*args, **kwargs):
        response = f(*args, **kwargs)
        response["Access-Control-Allow-Origin"] = "*"
        response["Access-Control-Allow-Methods"] = "GET, OPTIONS"
        response["Access-Control-Max-Age"] = "1000"
        response["Access-Control-Allow-Headers"] = "X-Requested-With, Content-Type"
        return response
    return wrapped


@allow_cross_origin
def get_game(request, pk):
    data = load_fixture('api__game__{}.json'.format(pk))
    return JsonResponse(data, status=200)


def get_initial_position(request):
    data = load_fixture('api__initial_position.json')
    return JsonResponse(data, status=200)
