import datetime as dt
from typing import Any

from beartype import beartype
from django.db.models import Count
from django.db.models import QuerySet


@beartype
def average_rating(rating_list: list[int], /) -> int:
    if len(rating_list) >= 1:
        return round(sum(rating_list) / len(rating_list))
    else:
        return 0


@beartype
def get_books_read_by_month(username: str, /) -> QuerySet[Any]:
    from reviews.models import Review

    current_year = dt.datetime.now().year
    return (
        Review.objects.filter(
            creator__username__contains=username,
            date_created__year=current_year,
        )
        .values("date_created__month")
        .annotate(book_count=Count("book__title"))
    )
