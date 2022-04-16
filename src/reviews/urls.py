from django.urls import include
from django.urls import path
from rest_framework.routers import DefaultRouter

from reviews.api_views import AllBooks
from reviews.api_views import ContributorView
from reviews.views import book_detail
from reviews.views import book_list
from reviews.views import book_media
from reviews.views import book_search
from reviews.views import index
from reviews.views import publisher_edit
from reviews.views import review_edit


router = DefaultRouter()
router.register("books", BookViewSet)
router.register("reviews", ReviewViewSet)


urlpatterns = [
    path("", index),
    path("api/all_books/", AllBooks.as_view(), name="all_books"),
    path("api/contributors/", ContributorView.as_view(), name="contributors"),
    path("books/", book_list, name=book_list.__name__),
    path("books/<int:pk>/", book_detail, name=book_detail.__name__),
    path("books/<int:pk>/media/", book_media, name=book_media.__name__),
    path("books/<int:book_pk>/reviews/new/", review_edit, name="review_create"),
    path(
        "books/<int:book_pk>/reviews/<int:review_pk>/",
        review_edit,
        name=review_edit.__name__,
    ),
    path("book-search/", book_search, name=book_search.__name__),
    path("publishers/<int:pk>/", publisher_edit, name=publisher_edit.__name__),
    path("publishers/new/", publisher_edit, name="publisher_create"),
]
