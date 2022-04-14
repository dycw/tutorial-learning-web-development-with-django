from beartype import beartype
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from reviews.models import Book


@beartype
def index(request: HttpRequest) -> HttpResponse:
    return render(
        request, "base.html", {"name": request.GET.get("name", "defname")}
    )


@beartype
def book_search(request: HttpRequest) -> HttpResponse:
    return render(
        request, "book_search.html", {"search": request.GET.get("search")}
    )


@beartype
def welcome_view(request: HttpRequest) -> HttpResponse:
    return render(request, "base.html")
    count = Book.objects.count()
    message = (
        f"<html><h1>Welcome to Bookr!</h1><p>{count} books and "
        + "counting!</p></html>"
    )
    return HttpResponse(message)
