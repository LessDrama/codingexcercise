from django.views.decorators.http import require_http_methods


# Create view url: /
@require_http_methods(["POST"])
def url_create_view(request):
    # When creating a short url:
    #   - it should generate a 10 char-length safe-url key.
    #   - it should return a data in json format.
    #   - it should return a CREATED status code.
    #   - it should be idempotent.
    #       - for idempotent, should return OK status code
    #         and the existing data.
    #   - it should validate the url (optional).
    #       - if fails, it should return a BAD REQUEST status code.
    ...


# Redirect url's url: /<key>
@require_http_methods(["GET"])
def url_redirect_view(request, key: str):
    # Each time you access a short url key e.g. http://localhost:8000/random-key:
    #   - it should redirect to the original url.
    #   - it should increase the view.
    #   - if short url not found, return a NOT FOUND status code.
    ...


# View url detail url: /<key>/detail
@require_http_methods(["GET"])
def url_detail_view(request, key: str):
    # When getting short url information:
    #   - it should return how many views the short url key has.
    #       - if not found, return a NOT FOUND status code.
    #   - it should return a data in json format.
    #   - it should return an OK status code.
    ...
