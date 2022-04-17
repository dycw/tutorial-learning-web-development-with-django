from typing import Any
from typing import cast

from django.contrib.auth.models import User
from django.utils import timezone
from rest_framework.exceptions import NotAuthenticated
from rest_framework.exceptions import PermissionDenied
from rest_framework.fields import SerializerMethodField
from rest_framework.relations import StringRelatedField
from rest_framework.serializers import ModelSerializer
from reviews.models import Book
from reviews.models import Publisher
from reviews.models import Review
from reviews.utils import average_rating


class PublisherSerializer(ModelSerializer):
    class Meta:
        model = Publisher
        fields = ["name", "website", "email"]


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ["username", "email"]


class ReviewSerializer(ModelSerializer):
    creator = UserSerializer(read_only=True)
    book = StringRelatedField(read_only=True)

    class Meta:
        model = Review
        fields = [
            "pk",
            "content",
            "date_created",
            "date_edited",
            "rating",
            "creator",
            "book",
            "book_id",
        ]

    def create(self, validated_data: Any) -> Any:
        request = self.context["request"]
        creator = request.user
        if not creator.is_authenticated:
            raise NotAuthenticated("Authentication required.")
        book = Book.objects.get(pk=request.data["book_id"])
        return Review.objects.create(
            content=validated_data["content"],
            book=book,
            creator=creator,
            rating=validated_data["rating"],
        )

    def update(self, instance: Any, validated_data: Any) -> Any:
        request = self.context["request"]
        creator = request.user
        if not creator.is_authenticated or instance.creator_id != creator.pk:
            raise PermissionDenied(
                "Permission denied, you are not the creator of this review"
            )
        instance.content = validated_data["content"]
        instance.rating = validated_data["rating"]
        instance.date_edited = timezone.now()
        instance.save()
        return instance


class BookSerializer(ModelSerializer):
    publisher = PublisherSerializer()
    rating = SerializerMethodField("book_rating")
    reviews = SerializerMethodField("book_reviews")

    def book_rating(self, book: Book) -> int | None:
        if reviews := cast(Any, book).review_set.all():
            return average_rating([review.rating for review in reviews])
        else:
            return None

    def book_reviews(self, book: Book) -> Any:
        if reviews := cast(Any, book).review_set.all():
            return ReviewSerializer(reviews, many=True).data
        else:
            return None

    class Meta:
        model = Book
        fields = [
            "title",
            "publication_date",
            "isbn",
            "publisher",
            "rating",
            "reviews",
        ]
