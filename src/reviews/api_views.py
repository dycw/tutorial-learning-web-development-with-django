from rest_framework.generics import ListAPIView

from reviews.models import Book
from reviews.models import Contributor
from reviews.serializers import BookSerializer
from reviews.serializers import ContributorSerializer


class AllBooks(ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer


class ContributorView(ListAPIView):
    queryset = Contributor.objects.all()
    serializer_class = ContributorSerializer
