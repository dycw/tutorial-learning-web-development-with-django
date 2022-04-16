from django.contrib.auth import get_user_model
from django.db.models import CASCADE
from django.db.models import CharField
from django.db.models import DateField
from django.db.models import DateTimeField
from django.db.models import EmailField
from django.db.models import FileField
from django.db.models import ForeignKey
from django.db.models import ImageField
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
    cover = ImageField(null=True, blank=True, upload_to="book_covers/")
    sample = FileField(null=True, blank=True, upload_to="book_samples/")

    def __str__(self) -> str:
        return f"{self.title} ({self.isbn})"

    def isbn13(self) -> str:
        """'9780316769174' => '978-0-31-676917-4'"""

        isbn = self.isbn
        return "-".join(
            [isbn[0:3], isbn[3:4], isbn[4:6], isbn[6:12], isbn[12:13]]
        )


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
        return self.initialled_name()

    def initialled_name(self) -> str:
        """self.first_names='Jerome David', self.last_names='Salinger'
        => 'Salinger, JD'"""

        initials = "".join([name[0] for name in self.first_names.split(" ")])
        return ", ".join([self.last_names, initials])

    def number_contributions(self) -> int:
        return self.bookcontributor_set.count()  # type: ignore


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

    def __str__(self) -> str:
        return " ".join(
            [self.contributor.initialled_name(), self.role, self.book.isbn]
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

    def __str__(self) -> str:
        return " - ".join([self.creator.username, self.book.title])
