from django.urls import path

from book_management.views import BookCreateView
from book_management.views import BookDeleteView
from book_management.views import BookRecordDetailView
from book_management.views import BookRecordFormView
from book_management.views import BookUpdateView
from book_management.views import FormSuccessView


urlpatterns = [
    path(
        "new_book_record/",
        BookRecordFormView.as_view(),
        name="book_record_form",
    ),
    path("entry_success/", FormSuccessView.as_view(), name="form_success"),
    path("book_record_create/", BookCreateView.as_view(), name="book_create"),
    path(
        "book_record_update/<int:pk>/",
        BookUpdateView.as_view(),
        name="book_update",
    ),
    path(
        "book_record_delete/<int:pk>/",
        BookDeleteView.as_view(),
        name="book_delete",
    ),
    path(
        "book_record_detail/<int:pk>/",
        BookRecordDetailView.as_view(),
        name="book_detail",
    ),
]
