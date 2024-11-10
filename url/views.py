from django.views.decorators.http import require_http_methods


@require_http_methods(["POST"])
def url_create_view(request, *args, **kwargs):
    # When creating a short url:
    #   - it should generate url-safe key.
    #       - the key should have 10 characters length.
    #   - it should return a data in json format.
    #   - it should return a CREATED status code.
    #   - it should be idempotent.
    #       - for idempotent, should return OK status code.
    #   - it should validate the url (optional).
    #       - if fails, it should return a BAD REQUEST status code.
    ...


@require_http_methods(["GET"])
def url_detail_view(request, key: str):
    # Each time you access a short url key:
    #   - it should return how many views has the short url key.
    #       - if not found, return a NOT FOUND status code.
    #   - it should return a data in json format.
    #   - it should return an OK status code.
    ...
