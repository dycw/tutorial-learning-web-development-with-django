from io import BytesIO
from typing import Any
from typing import cast

from beartype import beartype
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import AbstractUser
from django.contrib.messages import success
from django.core.exceptions import PermissionDenied
from django.core.files.images import ImageFile
from django.http import HttpRequest
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.shortcuts import redirect
from django.shortcuts import render
from django.utils.timezone import now
from PIL import Image
from reviews.forms import BookMediaForm
from reviews.forms import PublisherForm
from reviews.forms import ReviewForm
from reviews.forms import SearchForm
from reviews.models import Book
from reviews.models import Contributor
from reviews.models import Publisher
from reviews.models import Review
from reviews.utils import average_rating


@beartype
def index(request: HttpRequest) -> HttpResponse:
    viewed_books = [
        Book.objects.get(id=book_id)
        for book_id in request.session.get("viewed_books", [])
    ]
    context = {"viewed_books": viewed_books}
    return render(request, "reviews/index.html", context)


@beartype
def book_search(request: HttpRequest) -> HttpResponse:
    search_text = request.GET.get("search", "")
    books = set()
    if (form := SearchForm(request.GET)).is_valid():
        cleaned_data = form.cleaned_data
        if search := cleaned_data["search"]:
            if (cleaned_data.get("search_in") or "title") == "title":
                books |= set(Book.objects.filter(title__icontains=search))
            else:
                books |= set(
                    Contributor.objects.filter(first_names__icontains=search)
                    | Contributor.objects.filter(last_names__icontains=search)
                )
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
    book = cast(Any, get_object_or_404(Book, pk=pk))
    if reviews := cast(Any, book).review_set.all():
        book_rating = average_rating([review.rating for review in reviews])
        context = {"book": book, "book_rating": book_rating, "reviews": reviews}
    else:
        context = {"book": book, "book_rating": None, "reviews": None}
    if request.user.is_authenticated:
        max_viewed_books_length = 5
        viewed_books = request.session.get("viewed_books", [])
        if pk in viewed_books:
            viewed_books.pop(viewed_books.index(pk))
        _ = viewed_books.insert(0, pk)
        viewed_books = viewed_books[:max_viewed_books_length]
        request.session["viewed_books"] = viewed_books
    return render(request, "reviews/book_detail.html", context)


@beartype
def is_staff_user(user: AbstractUser) -> bool:
    return user.is_staff


@beartype
@user_passes_test(is_staff_user)
def publisher_edit(request: HttpRequest, pk: int | None = None) -> HttpResponse:
    if pk is None:
        publisher = None
    else:
        publisher = get_object_or_404(Publisher, pk=pk)
    if (request.method == "POST") and (
        form := PublisherForm(request.POST, instance=publisher)
    ).is_valid():
        updated_publisher = form.save()
        verb = "created" if publisher is None else "updated"
        success(request, f'Publisher "{updated_publisher}" was {verb}.')
        return redirect("publisher_detail", updated_publisher.pk)
    else:
        form = PublisherForm(instance=publisher)
    return render(
        request,
        "reviews/instance-form.html",
        {"form": form, "instance": publisher, "model_type": Publisher.__name__},
    )


@beartype
@login_required
def review_edit(
    request: HttpRequest, book_pk: int, review_pk: int | None = None
) -> HttpResponse:
    book = get_object_or_404(Book, pk=book_pk)
    if review_pk is None:
        review = None
    else:
        review = get_object_or_404(Review, book_id=book_pk, pk=review_pk)
        user = cast(Any, request.user)
        if not user.is_staff and review.creator.id != user.id:
            raise PermissionDenied
    if request.method == "POST":
        if (form := ReviewForm(request.POST, instance=review)).is_valid():
            updated_review = form.save(commit=False)
            updated_review.book = book
            if review is None:
                success(request, f'Review "{updated_review}" was created.')
            else:
                updated_review.date_edited = now()
                success(request, f'Review "{updated_review}" was updated.')
            updated_review.save()
            return redirect("book_detail", book.pk)
    else:
        form = ReviewForm(instance=review)
    return render(
        request,
        "reviews/instance-form.html",
        {
            "form": form,
            "instance": review_pk,
            "model_type": Review.__name__,
            "related_instance": book,
            "related_model_type": Book.__name__,
        },
    )


@beartype
@login_required
def book_media(request: HttpRequest, pk: int) -> HttpResponse:
    book = get_object_or_404(Book, pk=pk)
    if request.method == "POST":
        if (
            form := BookMediaForm(request.POST, request.FILES, instance=book)
        ).is_valid():
            book = form.save(commit=False)
            if cover := form.cleaned_data.get("cover"):
                image = Image.open(cover)
                image.thumbnail((300, 300))
                image_data = BytesIO()
                image.save(image_data, cover.image.format)
                image_file = ImageFile(image_data)
                book.cover.save(cover.name, image_file)
            book.save()
            success(request, f'Book "{book}" was successfully updated')
            return redirect("book_detail", book.pk)
    else:
        form = BookMediaForm(instance=book)
    return render(
        request,
        "reviews/instance-form.html",
        {"form": form, "instance": book, "model_type": Book.__name__},
    )


def react_example(request: HttpRequest) -> HttpResponse:
    return render(request, "react-example.html", {"name": "Ben", "target": 5})
