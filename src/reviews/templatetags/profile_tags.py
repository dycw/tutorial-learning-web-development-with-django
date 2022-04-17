from django.template import Library
from reviews.models import Review


register = Library()


@register.inclusion_tag("book_list.html")
def book_list(username: str) -> dict[str, list[str]]:
    reviews = Review.objects.filter(creator__username__contains=username)
    book_list = [review.book.title for review in reviews]
    return {"books_read": book_list}
