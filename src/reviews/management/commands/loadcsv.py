import csv  # noqa
import re

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from django.core.management.base import CommandError
from reviews.models import Book
from reviews.models import BookContributor
from reviews.models import Contributor
from reviews.models import Publisher
from reviews.models import Review


class Command(BaseCommand):
    help = "Load the reviews data from a CSV file."  # noqa

    def add_arguments(self, parser):  # type: ignore # noqa
        parser.add_argument("--csv", type=str)  # type: ignore

    @staticmethod
    def row_to_dict(row, header):  # type: ignore # noqa
        if len(row) < len(header):
            row += [""] * (len(header) - len(row))
        return {header[i]: row[i] for i, head in enumerate(header) if head}

    def handle(self, *args, **options):  # type: ignore # noqa
        m = re.compile(r"content:(\w+)")  # noqa
        header = None
        models = dict()  # noqa
        try:
            with open(options["csv"]) as csvfile:
                model_data = csv.reader(csvfile)
                for i, row in enumerate(model_data):  # type: ignore # noqa
                    if max(
                        len(cell.strip()) for cell in row[1:] + [""]
                    ) == 0 and m.match(row[0]):
                        model_name = m.match(row[0]).groups()[0]  # type: ignore
                        models[model_name] = []
                        header = None
                        continue

                    if header is None:
                        header = row
                        continue

                    row_dict = self.row_to_dict(row, header)
                    if set(row_dict.values()) == {""}:
                        continue
                    models[model_name].append(row_dict)  # type: ignore

        except FileNotFoundError:
            raise CommandError(
                'File "{}" does not exist'.format(options["csv"])
            )

        for data_dict in models.get("Publisher", []):
            p, created = Publisher.objects.get_or_create(
                name=data_dict["publisher_name"],
                defaults={
                    "website": data_dict["publisher_website"],
                    "email": data_dict["publisher_email"],
                },
            )

            if created:
                print(f'Created Publisher "{p.name}"')  # noqa

        for data_dict in models.get("Book", []):
            b, created = Book.objects.get_or_create(
                title=data_dict["book_title"],
                defaults={
                    "publication_date": data_dict[
                        "book_publication_date"
                    ].replace("/", "-"),
                    "isbn": data_dict["book_isbn"],
                    "publisher": Publisher.objects.get(
                        name=data_dict["book_publisher_name"]
                    ),
                },
            )

            if created:
                print(f'Created Publisher "{b.title}"')  # noqa

        for data_dict in models.get("Contributor", []):
            c, created = Contributor.objects.get_or_create(  # type: ignore
                first_names=data_dict["contributor_first_names"],
                last_names=data_dict["contributor_last_names"],
                email=data_dict["contributor_email"],
            )

            if created:
                print(  # noqa
                    'Created Contributor "{} {}"'.format(
                        data_dict["contributor_first_names"],
                        data_dict["contributor_last_names"],
                    )
                )

        for data_dict in models.get("BookContributor", []):
            book = Book.objects.get(title=data_dict["book_contributor_book"])
            contributor = Contributor.objects.get(
                email=data_dict["book_contributor_contributor"]
            )
            bc, created = BookContributor.objects.get_or_create(  # type: ignore
                book=book,
                contributor=contributor,
                role=data_dict["book_contributor_role"],
            )
            if created:
                print(  # noqa
                    f'Created BookContributor "{contributor.email}" -> "{book.title}"'
                )

        for data_dict in models.get("Review", []):
            creator, created = User.objects.get_or_create(
                email=data_dict["review_creator"],
                username=data_dict["review_creator"],
            )

            if created:
                print(f'Created User "{creator.email}"')  # noqa
            book = Book.objects.get(title=data_dict["review_book"])

            review, created = Review.objects.get_or_create(  # type: ignore
                content=data_dict["review_content"],
                book=book,
                creator=creator,
                defaults={
                    "rating": data_dict["review_rating"],
                    "date_created": data_dict["review_date_created"],
                    "date_edited": data_dict["review_date_edited"],
                },
            )
            if created:
                print(  # noqa
                    f'Created Review: "{book.title}" -> "{creator.email}"'
                )

        print("Import complete")  # noqa
