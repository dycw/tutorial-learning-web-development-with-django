from http import HTTPStatus

from django.test import RequestFactory
from django.test import TestCase

from reviews.views import index


class TestIndexView(TestCase):
    def setUp(self) -> None:
        self.factory = RequestFactory()

    def test_index_view(self) -> None:
        request = self.factory.get("/index")
        request.session = {}  # type: ignore
        response = index(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)
