import pytest
from app.core.logging_config import logger


def test_unauthorized_access(client):
    """
    Test unauthorized access to shorten URL endpoint.
    """

    response = client.post("/shorten")
    assert response.status_code == 401
    resp_json = response.json()
    assert resp_json["status"] == "error"
    assert resp_json["message"] == "API key is missing."


def test_shorten_url(client, user1_fixture):
    """
    Test if we can successfully shorten a URL.
    """

    response = client.post(
        "/shorten",
        headers={"x-api-key": user1_fixture.api_key},
        json={"original_url": "https://www.google.com"}
    )
    assert response.status_code == 200
    resp_json = response.json()
    assert resp_json["status"] == "success"
    assert "short_url" in resp_json["data"]
    assert resp_json["message"] == "URL shortened successfully."


def test_exist_original_url(client, user1_fixture):
    """
    Test if original URL already exist.
    """

    first_call = client.post(
        "/shorten",
        headers={"x-api-key": user1_fixture.api_key},
        json={"original_url": "https://www.google.com"}
    )
    assert first_call.status_code == 200

    second_call = client.post(
        "/shorten",
        headers={"x-api-key": user1_fixture.api_key},
        json={"original_url": "https://www.google.com"}
    )
    assert second_call.status_code == 200
    resp_json = second_call.json()
    assert resp_json["status"] == "success"
    assert "short_url" in resp_json["data"]
    assert resp_json["message"] == "URL already shortened for this user."


def test_redirect_url(client, user1_fixture):
    """
    Test redirect with the short code generated.
    """

    shorten_resp = client.post(
        "/shorten",
        headers={"x-api-key": user1_fixture.api_key},
        json={"original_url": "https://www.google.com"}
    )
    assert shorten_resp.status_code == 200
    short_url = shorten_resp.json()["data"]["short_url"]
    short_code = short_url.split("/")[-1]

    # Test redirect
    redirect_resp = client.get(
        f"/{short_code}",
        headers={"x-api-key": user1_fixture.api_key},
        allow_redirects=False
    )
    assert redirect_resp.status_code == 307


def test_rate_limit_exceeded(client, user2_fixture):
    """
    Test if daily rate limit is enforced.
    """

    for i in range(1, 52):
        resp = client.post(
            "/shorten",
            headers={"x-api-key": user2_fixture.api_key},
            json={"original_url": "https://test.com"}
        )
        if i <= 50:
            assert resp.status_code == 200
        else:
            assert resp.status_code == 429
            break
