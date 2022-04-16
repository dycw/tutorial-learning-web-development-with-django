from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet

from reviews.models import Book
from reviews.models import Review
from reviews.serializers import BookSerializer
from reviews.serializers import ReviewSerializer


class BookViewSet(ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.order_by("-date_created")
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = []
