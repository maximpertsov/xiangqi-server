import json
from http.cookies import SimpleCookie

from pytest import mark


# TODO: mock successfully refreshed access token

@mark.django_db
@mark.skip
def test_refresh_failed(client, player):
    client.cookies = SimpleCookie({"refresh": "REFRESH_TOKEN"})
    response = client.post(
        "/api/token/refresh", data=None, content_type="application/json"
    )
    assert response.status_code == 401


@mark.django_db
@mark.skip
def test_obtain_token(client, player):
    password = "pass123"
    player.set_password(password)
    player.save()

    data = {"username": player.username, "password": password}

    response = client.post(
        "/api/token/obtain", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 200
    assert set(response.data.keys()) == set(["token"])


@mark.django_db
@mark.skip
def test_obtain_token_failed(client, player):
    password = "pass123"
    player.set_password(password)
    player.save()

    data = {"username": player.username, "password": "badpassword"}

    response = client.post(
        "/api/token/obtain", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 401
