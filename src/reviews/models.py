from django.db.models import CharField
from django.db.models import EmailField
from django.db.models import Model
from django.db.models import URLField


class Publisher(Model):
    """A company that publishes books."""

    name = CharField(max_length=50, help_text="The name of the Publisher.")
    website = URLField(help_text="The Publisher's website.")
    email = EmailField(help_text="The Publisher's email address.")
