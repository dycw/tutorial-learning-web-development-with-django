from typing import Any
from typing import TYPE_CHECKING
from typing import TypeVar

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from django.db.models import Model
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

    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        self.helper.add_input(Submit("", "Search"))


_M = TypeVar("_M", bound=Model)


class InstanceForm(ModelForm[_M] if TYPE_CHECKING else ModelForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super().__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_method = "get"
        button_title = "Save" if "instance" in kwargs else "Create"
        self.helper.add_input(Submit("", button_title))


class PublisherForm(InstanceForm[Publisher] if TYPE_CHECKING else InstanceForm):
    class Meta:  # type: ignore
        model = Publisher
        fields = "__all__"


class ReviewForm(InstanceForm[Review] if TYPE_CHECKING else InstanceForm):
    class Meta:  # type: ignore
        model = Review
        exclude = ["date_edited", "book"]

    rating = IntegerField(min_value=0, max_value=5)


class BookMediaForm(InstanceForm[Book] if TYPE_CHECKING else InstanceForm):
    class Meta:  # type: ignore
        model = Book
        fields = ["cover", "sample"]
