from rest_framework.serializers import CharField
from rest_framework.serializers import DateField
from rest_framework.serializers import EmailField
from rest_framework.serializers import Serializer
from rest_framework.serializers import URLField


class PublisherSerializer(Serializer):  # type: ignore
    name = CharField()
    website = URLField()
    email = EmailField()


class BookSerializer(Serializer):  # type: ignore
    name = CharField()
    publication_date = DateField()
    isbn = CharField()
    publisher = PublisherSerializer()
