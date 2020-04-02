import json

from pytest import mark


@mark.django_db
@mark.skip("Requires cookies in request")
def test_authenticate(client, user):
    password = "s0_s0_secure"
    user.set_password(password)
    user.save()

    data = {"username": user.username, "password": password}

    r = client.post(
        "/api/authenticate", data=json.dumps(data), content_type="application/json"
    )
    assert r.status_code == 201
    response_data = r.json()
    assert "access_token" in response_data


@mark.django_db
def test_login(client, user):
    password = "s0_s0_secure"
    user.set_password(password)
    user.save()

    assert user.accesstoken_set.count() == 0
    assert user.refreshtoken_set.count() == 0

    data = {"username": user.username, "password": password}

    response = client.post(
        "/api/login", data=json.dumps(data), content_type="application/json"
    )
    assert response.status_code == 201

    cookies = response.client.cookies
    assert "access_token" in cookies
    assert "refresh_token" in cookies

    assert user.accesstoken_set.count() == 1
    assert user.refreshtoken_set.count() == 1
