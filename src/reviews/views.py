from beartype import beartype
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import render

from reviews.models import Book
from reviews.utils import average_rating


@beartype
def book_list(request: HttpRequest) -> HttpResponse:
    books = Book.objects.all()
    book_list = []
    for book in books:
        if reviews := book.review_set.all():
            book_rating = average_rating([review.rating for review in reviews])
            number_of_reviews = len(reviews)
        else:
            book_rating = None
            number_of_reviews = 0
        book_list.append(
            {
                "book": book,
                "book_rating": book_rating,
                "number_of_reviews": number_of_reviews,
            }
        )
    context = {"book_list": book_list}
    return render(request, "reviews/books_list.html", context)
