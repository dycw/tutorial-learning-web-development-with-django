from beartype import beartype
from django.http.request import HttpRequest
from django.http.response import HttpResponse
from django.shortcuts import render


@beartype
def index(request: HttpRequest) -> HttpResponse:
    return render(
        request, "base.html", {"name": request.GET.get("name", "defname")}
    )


@beartype
def book_search(request: HttpRequest) -> HttpResponse:
    return render(request, "book_search.html")
