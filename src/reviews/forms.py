from typing import TYPE_CHECKING

from django.forms import CharField
from django.forms import ChoiceField
from django.forms import Form
from django.forms import IntegerField
from django.forms import ModelForm

from reviews.models import Book
from reviews.models import Publisher
from reviews.models import Review


class SearchForm(Form):
    search = CharField(required=False, min_length=3)
    search_in = ChoiceField(
        required=False,
        choices=(("title", "Title"), ("contributor", "Contributor")),
    )


class PublisherForm(ModelForm[Publisher] if TYPE_CHECKING else ModelForm):
    class Meta:  # type: ignore
        model = Publisher
        fields = "__all__"


class ReviewForm(ModelForm[Review] if TYPE_CHECKING else ModelForm):
    class Meta:  # type: ignore
        model = Review
        exclude = ["date_edited", "book"]

    rating = IntegerField(min_value=0, max_value=5)


class BookMediaForm(ModelForm[Book] if TYPE_CHECKING else ModelForm):
    class Meta:  # type: ignore
        model = Book
        fields = ["cover", "sample"]
