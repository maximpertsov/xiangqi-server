import json

from pytest import mark


@mark.django_db
@mark.skip("Requires cookies in request")
def test_authenticate(client, player):
    password = "s0_s0_secure"
    player.set_password(password)
    player.save()

    data = {"username": player.username, "password": password}

    r = client.post(
        "/api/authenticate", data=json.dumps(data), content_type="application/json"
    )
    assert r.status_code == 201
    response_data = r.json()
    assert "access_token" in response_data


@mark.django_db
def test_login(client, player):
    password = "s0_s0_secure"
    player.set_password(password)
    player.save()

    assert player.accesstoken_set.count() == 0
    assert player.refreshtoken_set.count() == 0

    data = {"username": player.username, "password": password}

    response = client.post(
        "/api/login", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201

    cookies = response.client.cookies
    assert "access_token" in cookies
    assert "refresh_token" in cookies

    assert player.accesstoken_set.count() == 1
    assert player.refreshtoken_set.count() == 1
