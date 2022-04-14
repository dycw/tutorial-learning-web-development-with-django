from django.urls import path

from reviews.views import book_detail
from reviews.views import book_list
from reviews.views import book_search
from reviews.views import index


urlpatterns = [
    path("", index),
    path("books/", book_list, name="book_list"),
    path("books/<int:pk>/", book_detail, name="book_detail"),
    path("book-search/", book_search, name="book_search"),
]
