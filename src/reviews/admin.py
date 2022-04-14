from typing import TYPE_CHECKING
from typing import Any

from django.contrib.admin import ModelAdmin as _ModelAdmin
from django.contrib.admin import site

from reviews.models import Book
from reviews.models import BookContributor
from reviews.models import Contributor
from reviews.models import Publisher
from reviews.models import Review


ModelAdmin = _ModelAdmin[Any] if TYPE_CHECKING else _ModelAdmin


class BookAdmin(ModelAdmin):
    date_hierarchy = "publication_date"
    list_display = ("title", "isbn")
    # or: >>> list_display = ("title", "isbn13")
    list_filter = ("publisher", "publication_date")


def initialled_name(obj: Contributor, /) -> str:
    """obj.first_names='Jerome David', obj.last_names='Salinger'
    => 'Salinger, JD'"""
    initials = "".join([name[0] for name in obj.first_names.split(" ")])
    return f"{obj.last_names}, {initials}"


class ContributorAdmin(ModelAdmin):
    list_display = ("last_names", "first_names")
    # or: >>> list_display = (initialled_name,)
    list_filter = ("last_names",)
    search_fields = ("last_names__startswith", "first_names")


site.register(Publisher)
site.register(Contributor, ContributorAdmin)
site.register(Book, BookAdmin)
site.register(BookContributor)
site.register(Review)
