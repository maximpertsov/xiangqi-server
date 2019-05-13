from django.shortcuts import render
import json
from django.http import JsonResponse


def get_game(request, pk):
    data = """
{
    "players": [
        {
            "color": "red",
            "name": "max"
        },
        {
            "color": "black",
            "name": "jason"
        }
    ]
}
    """
    return JsonResponse(json.loads(data), status=200)


def get_initial_position(request):
    data = """
{
  "pieces": [
    {
      "code": "r",
      "file": 0,
      "rank": 0
    },
    {
      "code": "h",
      "file": 1,
      "rank": 0
    },
    {
      "code": "e",
      "file": 2,
      "rank": 0
    },
    {
      "code": "a",
      "file": 3,
      "rank": 0
    },
    {
      "code": "k",
      "file": 4,
      "rank": 0
    },
    {
      "code": "a",
      "file": 5,
      "rank": 0
    },
    {
      "code": "e",
      "file": 6,
      "rank": 0
    },
    {
      "code": "h",
      "file": 7,
      "rank": 0
    },
    {
      "code": "r",
      "file": 8,
      "rank": 0
    },
    {
      "code": "c",
      "file": 1,
      "rank": 2
    },
    {
      "code": "c",
      "file": 7,
      "rank": 2
    },
    {
      "code": "p",
      "file": 0,
      "rank": 3
    },
    {
      "code": "p",
      "file": 2,
      "rank": 3
    },
    {
      "code": "p",
      "file": 4,
      "rank": 3
    },
    {
      "code": "p",
      "file": 6,
      "rank": 3
    },
    {
      "code": "p",
      "file": 8,
      "rank": 3
    },
    {
      "code": "P",
      "file": 0,
      "rank": 6
    },
    {
      "code": "P",
      "file": 2,
      "rank": 6
    },
    {
      "code": "P",
      "file": 4,
      "rank": 6
    },
    {
      "code": "P",
      "file": 6,
      "rank": 6
    },
    {
      "code": "P",
      "file": 8,
      "rank": 6
    },
    {
      "code": "C",
      "file": 1,
      "rank": 7
    },
    {
      "code": "C",
      "file": 7,
      "rank": 7
    },
    {
      "code": "R",
      "file": 0,
      "rank": 9
    },
    {
      "code": "H",
      "file": 1,
      "rank": 9
    },
    {
      "code": "E",
      "file": 2,
      "rank": 9
    },
    {
      "code": "A",
      "file": 3,
      "rank": 9
    },
    {
      "code": "K",
      "file": 4,
      "rank": 9
    },
    {
      "code": "A",
      "file": 5,
      "rank": 9
    },
    {
      "code": "E",
      "file": 6,
      "rank": 9
    },
    {
      "code": "H",
      "file": 7,
      "rank": 9
    },
    {
      "code": "R",
      "file": 8,
      "rank": 9
    }
  ]
}
    """
    return JsonResponse(json.loads(data), status=200)
