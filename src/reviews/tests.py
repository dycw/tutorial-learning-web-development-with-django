from django.test import TestCase


class TestSimpleComponent(TestCase):
    def test_basic(self) -> None:
        self.assertEqual(1 + 1, 2)
