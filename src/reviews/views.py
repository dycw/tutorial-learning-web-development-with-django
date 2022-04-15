from typing import Any
from typing import cast

from beartype import beartype
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from reviews.models import Book
from reviews.utils import average_rating


@beartype
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "base.html")


@beartype
def book_search(request: HttpRequest) -> HttpResponse:
    search_text = request.GET.get("search", "")
    return render(
        request, "reviews/search-results.html", {"search_text": search_text}
    )


@beartype
def book_list(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all()
    books_with_reviews = []
    for book in books:
        if reviews := cast(Any, book).review_set.all():
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        books_with_reviews.append(
            {
                "book": book,
                "book_rating": book_rating,
                "number_of_reviews": number_of_reviews,
            }
        )
    context = {"book_list": books_with_reviews}
    return render(request, "reviews/book_list.html", context)


@beartype
def book_detail(request: HttpRequest, pk: int) -> HttpResponse:
    book = get_object_or_404(Book, pk=pk)
    if reviews := cast(Any, book).review_set.all():
        book_rating = average_rating([review.rating for review in reviews])
        context = {"book": book, "book_rating": book_rating, "reviews": reviews}
    else:
        context = {"book": book, "book_rating": None, "reviews": None}
    return render(request, "reviews/book_detail.html", context)
