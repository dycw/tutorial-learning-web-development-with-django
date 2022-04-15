from typing import TYPE_CHECKING
from typing import Any

from django.forms import CharField
from django.forms import ChoiceField
from django.forms import Form
from django.forms import ModelForm as _ModelForm

from reviews.models import Publisher


ModelForm = _ModelForm[Any] if TYPE_CHECKING else _ModelForm


class SearchForm(Form):
    search = CharField(required=False, min_length=3)
    search_in = ChoiceField(
        required=False,
        choices=(("title", "Title"), ("contributor", "Contributor")),
    )


class PublisherForm(ModelForm):
    class Meta:  # type: ignore
        model = Publisher
        fields = "__all__"
