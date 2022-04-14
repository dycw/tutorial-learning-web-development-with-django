from beartype import beartype
from django.http.request import HttpRequest
from django.http.response import HttpResponse


@beartype
def index(_: HttpRequest) -> HttpResponse:
    return HttpResponse("Hello, world!")
