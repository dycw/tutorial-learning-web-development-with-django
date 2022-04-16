from typing import TYPE_CHECKING
from typing import Any

from beartype import beartype
from django.http import HttpRequest
from django.http import HttpResponse
from django.views import View
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import FormView
from django.views.generic import UpdateView

from book_management.forms import BookForm
from book_management.models import Book


class BookRecordFormView(FormView[BookForm] if TYPE_CHECKING else FormView):
    template_name = "book_form.html"
    form_class = BookForm
    success_url = "/book_management/entry_success"

    @beartype
    def form_valid(self, form: BookForm) -> HttpResponse:
        _ = form.save()
        return super().form_valid(form)


class FormSuccessView(View):
    @beartype
    def get(self, _: HttpRequest, *args: Any, **kwargs: Any) -> HttpResponse:
        return HttpResponse("Book record saved successfully")


class BookCreateView(
    CreateView[Book, BookForm] if TYPE_CHECKING else CreateView
):
    model = Book
    fields = ["name", "author"]
    template_name = "book_form.html"
    success_url = "/book_management/entry_success"


class BookUpdateView(
    UpdateView[Book, BookForm] if TYPE_CHECKING else UpdateView
):
    model = Book
    fields = ["name", "author"]
    template_name = "book_form.html"
    success_url = "/book_management/entry_success"


class BookDeleteView(DeleteView):
    model = Book
    template_name = "book_delete_form.html"
    success_url = "/book_management/delete_success"


class BookRecordDetailView(DetailView[Book] if TYPE_CHECKING else DetailView):
    model = Book
    template_name = "book_detail.html"
