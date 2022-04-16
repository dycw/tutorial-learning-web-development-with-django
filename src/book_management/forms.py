from typing import TYPE_CHECKING

from django.forms import ModelForm

from book_management.models import Book


class BookForm(ModelForm[Book] if TYPE_CHECKING else ModelForm):
    class Meta:  # type: ignore
        model = Book
        fields = ["name", "author"]
