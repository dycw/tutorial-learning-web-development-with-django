from django.urls import path

from book_management.views import BookRecordFormView
from book_management.views import FormSuccessView


urlpatterns = [
    path(
        "new_book_record", BookRecordFormView.as_view(), name="book_record_form"
    ),
    path("entry_success", FormSuccessView.as_view(), name="form_success"),
]
