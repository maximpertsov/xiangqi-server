import json
from http.cookies import SimpleCookie

from pytest import mark


@mark.django_db
def test_authenticate(client, player):
    client.cookies = SimpleCookie({"refresh": "REFRESH_TOKEN"})
    response = client.post(
        "/api/token/refresh", data=None, content_type="application/json"
    )
    assert response.status_code == 200
    print(response.json())
    assert "access_token" in response.json()


@mark.django_db
def test_obtain_token(client, player):
    password = "pass123"
    player.set_password(password)
    player.save()

    data = {"username": player.username, "password": password}

    response = client.post(
        "/api/token/obtain", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 200
    assert set(response.data.keys()) == set(["access", "refresh"])


@mark.django_db
def test_obtain_token_failed(client, player):
    password = "pass123"
    player.set_password(password)
    player.save()

    data = {"username": player.username, "password": "badpassword"}

    response = client.post(
        "/api/token/obtain", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 401
