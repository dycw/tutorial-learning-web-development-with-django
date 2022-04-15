from typing import Any
from typing import cast

from beartype import beartype
from django.contrib.messages import success
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render

from reviews.forms import PublisherForm
from reviews.forms import SearchForm
from reviews.models import Book
from reviews.models import Contributor
from reviews.models import Publisher
from reviews.utils import average_rating


@beartype
def index(request: HttpRequest) -> HttpResponse:
    return render(request, "base.html")


@beartype
def book_search(request: HttpRequest) -> HttpResponse:
    search_text = request.GET.get("search", "")
    form = SearchForm(request.GET)
    if form.is_valid():
        cleaned_data = form.cleaned_data
        if search := cleaned_data["search"]:
            if (cleaned_data.get("search_in") or "title") == "title":
                books = Book.objects.filter(title__icontains=search)
            else:
                books = set(
                    Contributor.objects.filter(first_names__icontains=search)
                    | Contributor.objects.filter(last_names__icontains=search)
                )
        else:
            books = set()
    else:
        books = set()
    return render(
        request,
        "reviews/search-results.html",
        {"form": form, "search_text": search_text, "books": books},
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


@beartype
def publisher_edit(request: HttpRequest, pk: int | None = None) -> HttpResponse:
    if pk is None:
        publisher = None
    else:
        publisher = get_object_or_404(Publisher, pk=pk)
    if (request.method == "POST") and (
        form := PublisherForm(request.POST, instance=publisher)
    ).is_valid():
        updated_publisher = form.save()
        if publisher is None:
            success(request, f'Publisher "{updated_publisher}" was created.')
        else:
            success(request, f'Publisher "{updated_publisher}" was updated.')
        return redirect("publisher_edit", updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)
    return render(
        request, "form-example.html", {"method": request.method, "form": form}
    )
