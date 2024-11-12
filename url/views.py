import random
import string
from http import HTTPStatus

from django.core.exceptions import ValidationError
from django.core.validators import URLValidator
from django.http import HttpResponseRedirect
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods

from url.models import Url


def generate_key():
    return ''.join(random.choices(string.ascii_letters + string.digits, k=10))


# Create view url: /
@require_http_methods(["POST"])
def url_create_view(request):
    data = request.POST.get('url')

    validator = URLValidator()
    try:
        validator(data)
    except ValidationError:
        return JsonResponse({'error': 'Invalid URL'}, status=400)

    # Check if the URL already exists
    url_instance = Url.objects.filter(url=data).first()
    if url_instance:
        return JsonResponse({'shortUrl': f'http://localhost:8000/{url_instance.key}'}, status=HTTPStatus.OK)

    key = generate_key()
    url_instance = Url.objects.create(url=data, key=key)
    return JsonResponse({'shortUrl': f'http://localhost:8000/{url_instance.key}'}, status=HTTPStatus.CREATED)


# Redirect url's url: /<key>
@require_http_methods(["GET"])
def url_redirect_view(request, key: str):
    try:
        url_instance = Url.objects.get(key=key)
    except Url.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=HTTPStatus.NOT_FOUND)

    url_instance.views += 1
    url_instance.save()

    return HttpResponseRedirect(url_instance.url)


# View url detail url: /<key>/detail
@require_http_methods(["GET"])
def url_detail_view(request, key: str):
    try:
        url_instance = Url.objects.get(key=key)
    except Url.DoesNotExist:
        return JsonResponse({'error': 'Not found'}, status=HTTPStatus.NOT_FOUND)

    return JsonResponse({'url': url_instance.url, 'views': url_instance.views}, status=HTTPStatus.OK)
