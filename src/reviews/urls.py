from django.urls import path

from reviews.views import book_detail
from reviews.views import book_list
from reviews.views import book_search
from reviews.views import index
from reviews.views import publisher_edit


urlpatterns = [
    path("", index),
    path("books/", book_list, name=book_list.__name__),
    path("books/<int:pk>/", book_detail, name=book_detail.__name__),
    path("book-search/", book_search, name=book_search.__name__),
    path("publishers/<int:pk>/", publisher_edit, name=publisher_edit.__name__),
    path("publishers/new/", publisher_edit, name="publisher_create"),
]
