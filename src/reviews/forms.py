from django.forms import CharField
from django.forms import ChoiceField
from django.forms import Form


class SearchForm(Form):
    search = CharField(required=False, min_length=3)
    search_in = ChoiceField(
        required=False,
        choices=(("title", "Title"), ("contributor", "Contributor")),
    )
