from rest_framework.fields import ReadOnlyField
from rest_framework.serializers import ModelSerializer

from reviews.models import Book
from reviews.models import BookContributor
from reviews.models import Contributor
from reviews.models import Publisher


class PublisherSerializer(ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["name", "website", "email"]


class BookSerializer(ModelSerializer):
    publisher = PublisherSerializer()

    class Meta:
        model = Book
        fields = ["title", "publication_date", "isbn", "publisher"]


class ContributionSerializer(ModelSerializer):
    book = BookSerializer()

    class Meta:
        model = BookContributor
        fields = ["book", "role"]


class ContributorSerializer(ModelSerializer):
    bookcontributor_set = ContributionSerializer(read_only=True, many=True)
    number_contributions = ReadOnlyField()

    class Meta:
        model = Contributor
        fields = [
            "first_names",
            "last_names",
            "email",
            "bookcontributor_set",
            "number_contributions",
        ]
