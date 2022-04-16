from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response

from reviews.models import Book


@api_view()  # type: ignore
def first_api_view(_: HttpRequest) -> Response:
    num_books = Book.objects.count()
    return Response({"num_books": num_books})
