from typing import Any
from typing import cast

from django.contrib.auth import authenticate
from rest_framework.authtoken.models import Token
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.viewsets import ReadOnlyModelViewSet
from reviews.models import Book
from reviews.models import Review
from reviews.serializers import BookSerializer
from reviews.serializers import ReviewSerializer


class Login(APIView):
    def post(self, request: Request) -> Response:  # type: ignore
        data = cast(Any, request.data)
        user = authenticate(
            username=data.get("username"), password=data.get("password")
        )
        if not user:
            return Response(
                {"error": "Credentials are incorrect or user does not exist"},
                status=HTTP_404_NOT_FOUND,
            )
        token, _ = Token.objects.get_or_create(user=user)
        return Response({"token": token.key}, status=HTTP_200_OK)


class BookViewSet(ReadOnlyModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    authentication_classes = []
    permission_classes = []
    # >>> authentication_classes = [TokenAuthentication]
    # >>> permission_classes = [IsAuthenticated]


class ReviewViewSet(ModelViewSet):
    queryset = Review.objects.order_by("-date_created")
    serializer_class = ReviewSerializer
    pagination_class = LimitOffsetPagination
    authentication_classes = []
