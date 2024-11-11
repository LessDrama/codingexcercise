from django.views.decorators.http import require_http_methods


# Create view url: /
@require_http_methods(["POST"])
def url_create_view(request):
    ...


# Redirect url's url: /<key>
@require_http_methods(["GET"])
def url_redirect_view(request, key: str):
    ...


# View url detail url: /<key>/detail
@require_http_methods(["GET"])
def url_detail_view(request, key: str):
    ...
