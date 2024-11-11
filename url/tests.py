import random
from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse

from url.models import Url

pytestmark = pytest.mark.django_db


@pytest.fixture
def short_url() -> Url:
    return Url.objects.create(
        url="https://example.com/long-url-description",
        key="random-key",
    )


def test_create_short_url(client: Client):
    url = reverse("url-create")
    response = client.post(
        path=url,
        data={"url": "https://example.com/long-url-description"},
    )
    assert (
        response.status_code == HTTPStatus.CREATED
    ), "Creating short url did not return a CREATED status."

    data = response.json()

    url_key = data["shortUrl"][-10:]
    assert Url.objects.filter(
        key=url_key
    ).exists(), "Short url key was not created properly, check the created key."


def test_create_short_url_idempotent(client: Client, short_url: Url):
    url = reverse("url-create")
    response = client.post(
        path=url,
        data={"url": "https://example.com/long-url-description"},
    )
    assert (
        response.status_code == HTTPStatus.OK
    ), "Creating idempotent short url did not return an OK status."

    assert Url.objects.count() == 1, "Not idempotent, it created more than 1 records."


def test_create_short_url_invalid_url(client: Client):
    url = reverse("url-create")
    response = client.post(
        path=url,
        data={"url": "abcd://example/invalid-url"},
    )
    assert (
        response.status_code == HTTPStatus.BAD_REQUEST
    ), "Creating invalid short url did not return a BAD REQUEST status."


def test_redirect_short_url(client: Client, short_url: Url):
    url = reverse("url-redirect", kwargs={"key": short_url.key})
    detail_response = client.get(path=url)
    assert detail_response.status_code == HTTPStatus.FOUND, "Not re-directed."


def test_redirect_short_url_not_found(client: Client, short_url: Url):
    url = reverse("url-redirect", kwargs={"key": short_url.key[:3]})
    detail_response = client.get(path=url)
    assert (
        detail_response.status_code == HTTPStatus.NOT_FOUND
    ), "Did not return NOT FOUND status code."


def test_get_short_url(client: Client, short_url: Url):
    views = random.randint(1, 100)
    for _ in range(views):
        url = reverse("url-redirect", kwargs={"key": short_url.key})
        client.get(path=url)

    short_url.refresh_from_db(fields=["views"])
    assert (
        short_url.views == views
    ), f"It returned {short_url.views} views, but expected {views} views."


def test_get_short_url_not_found(client: Client, short_url: Url):
    # The short_url_key always have a 10 characters len.
    url = reverse("url-detail", kwargs={"key": short_url.key[:3]})
    detail_response = client.get(path=url)
    assert (
        detail_response.status_code == HTTPStatus.NOT_FOUND
    ), "Did not return NOT FOUND status."
