from django.http import HttpRequest
from rest_framework.decorators import api_view
from rest_framework.response import Response

from reviews.models import Book
from reviews.serializers import BookSerializer


@api_view()  # type: ignore
def all_books(_: HttpRequest) -> Response:
    books = Book.objects.all()
    book_serializer = BookSerializer(books, many=True)
    return Response(book_serializer.data)
