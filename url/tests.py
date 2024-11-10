import random
from http import HTTPStatus

import pytest
from django.test.client import Client
from django.urls import reverse
from url.models import Url

pytestmark = pytest.mark.django_db


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
    shorturl_data = data["shortUrl"].split("/shorturl/")
    assert len(shorturl_data[1]) == 8, "The short url don't have 8 characters length"


def test_create_short_url_idempotent(client: Client):
    url = reverse("url-create")
    response_1 = client.post(
        path=url,
        data={"url": "https://example.com/long-url-description"},
    )
    assert (
        response_1.status_code == HTTPStatus.CREATED
    ), "Creating short url did not return a CREATED status."

    response_2 = client.post(
        path=url,
        data={"url": "https://example.com/long-url-description"},
    )
    assert (
        response_2.status_code == HTTPStatus.OK
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


def test_get_short_url(client: Client):
    url = reverse("url-create")
    create_response = client.post(
        path=url,
        data={"url": "https://example.com/long-url-description"},
    )
    assert (
        create_response.status_code == HTTPStatus.CREATED
    ), "Creating short url did not return a CREATED status."
    short_url_data = create_response.json()

    short_url_key = short_url_data["shortUrl"].split("/shorturl/")[1]

    views = random.randint(1, 100)
    for _ in range(views):
        url = reverse("url-detail", kwargs={"key": short_url_key})
        detail_response = client.get(path=url)

    view_data = detail_response.json()
    assert (
        view_data["views"] == views
    ), f"It returned {view_data['views']} views, but expected {views} views."


def test_get_short_url_not_found(client: Client):
    url = reverse("url-create")
    create_response = client.post(
        path=url,
        data={"url": "https://example.com/long-url-description"},
    )
    assert (
        create_response.status_code == HTTPStatus.CREATED
    ), "Creating short url did not return a CREATED status."
    short_url_data = create_response.json()

    short_url_key = short_url_data["shortUrl"].split("/shorturl/")[1]

    # The short_url_key always have a 8 characters len.
    url = reverse("url-detail", kwargs={"key": short_url_key[:3]})
    detail_response = client.get(path=url)
    assert (
        detail_response.status_code == HTTPStatus.NOT_FOUND
    ), "Did not return NOT FOUND status."
