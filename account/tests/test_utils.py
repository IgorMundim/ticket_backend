from unittest import TestCase

from django.core.exceptions import ValidationError
from utils.validation import strong_password


class UtilsTest(TestCase):
    def setUp(self) -> None:
        return super().setUp()

    def test_strong_password(self):
        with self.assertRaises(ValidationError):
            strong_password("12345")
        self.assertIsNone(strong_password("@Abc12345"))