from django.contrib.auth import get_user_model
from django.db.models import CASCADE
from django.db.models import CharField
from django.db.models import DateField
from django.db.models import DateTimeField
from django.db.models import EmailField
from django.db.models import ForeignKey
from django.db.models import IntegerField
from django.db.models import ManyToManyField
from django.db.models import Model
from django.db.models import TextChoices
from django.db.models import TextField
from django.db.models import URLField


class Publisher(Model):
    """A company that publishes books."""

    name = CharField(max_length=50, help_text="The name of the Publisher.")
    website = URLField(help_text="The Publisher's website.")
    email = EmailField(help_text="The Publisher's email address.")

    def __str__(self) -> str:
        return self.name


class Book(Model):
    """A published book."""

    title = CharField(max_length=70, help_text="The title of the book.")
    publication_date = DateField(verbose_name="Date the book was published.")
    isbn = CharField(max_length=20, verbose_name="ISBN number of the book.")
    publisher = ForeignKey(Publisher, on_delete=CASCADE)
    contributors = ManyToManyField("Contributor", through="BookContributor")

    def __str__(self) -> str:
        return self.title


class Contributor(Model):
    """A contributor to a Book, e.g. author, editor, co-author."""

    first_names = CharField(
        max_length=50, help_text="The contributor's first name or names."
    )
    last_names = CharField(
        max_length=50, help_text="The contributor's last name or names."
    )
    email = EmailField(help_text="The contact email for the contributor.")

    def __str__(self) -> str:
        return self.first_names


class BookContributor(Model):
    class ContributionRole(TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-Author"
        EDITOR = "EDITOR", "Editor"

    book = ForeignKey(Book, on_delete=CASCADE)
    contributor = ForeignKey(Contributor, on_delete=CASCADE)
    role = CharField(
        verbose_name="The role this contributor had in the book",
        choices=ContributionRole.choices,
        max_length=20,
    )


class Review(Model):
    content = TextField(help_text="The Review text.")
    rating = IntegerField(help_text="The rating the reviewer has given.")
    date_created = DateTimeField(
        auto_now_add=True, help_text="The date and time the review was created."
    )
    date_edited = DateTimeField(
        null=True, help_text="The date and time the review was last edited."
    )
    creator = ForeignKey(get_user_model(), on_delete=CASCADE)
    book = ForeignKey(
        Book, on_delete=CASCADE, help_text="The Book that this review is for."
    )
