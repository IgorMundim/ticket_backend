from django.urls import reverse
from rest_framework import test

from account.tests.test_account_base import AccountMixin
from event.tests.test_event_base import EventMixin


class EventApiv1TestCategory(test.APITestCase, EventMixin, AccountMixin):
    def setUp(self) -> None:
        self.category_data = {
            "name": "Test Post",
            "slug": "test_post",
            "is_active": "true",
            "alt_text": "Test post",
        }
        self.app()
        return super().setUp()

    def test_categories_api_list_returns_status_code_200(self):
        response = self.client.get(reverse("event:categories-list-create"))
        self.assertEqual(response.status_code, 200)

    def test_category_api_list_do_not_activate(self):
        self.make_category(name="Active", slug="active", is_active=True)
        self.make_category(
            name="Not Active", slug="not-active", is_active=False
        )
        response = self.client.get(reverse("event:categories-list-create"))
        self.assertEqual(len(response.data), 1)

    def test_create_category_with_anonymous_user(self):

        response = self.client.post(
            reverse("event:categories-list-create"),
            data=self.category_data,
        )

        self.assertEqual(response.status_code, 401)

    def test_create_category_with_simple_user(self):
        response = self.client.post(
            reverse("event:categories-list-create"),
            data=self.category_data,
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_simple_user()}",  # noqa: E501
        )
        self.assertEqual(response.status_code, 403)

    def test_create_category_with_super_user(self):

        response = self.client.post(
            reverse("event:categories-list-create"),
            data=self.category_data,
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_super_user()}",  # noqa: E501
        )
        self.assertEqual(response.status_code, 201)

    def test_update_category_with_anonymous_user(self):
        self.category = self.make_category()
        response = self.client.patch(
            reverse(
                "event:category-retrieve-update", args=(self.category.id,)
            ),
            data={"alt_text": "Change"},
        )
        self.assertEqual(response.status_code, 401)

    def test_update_with_simple_user(self):
        self.category = self.make_category()
        response = self.client.patch(
            reverse(
                "event:category-retrieve-update", args=(self.category.id,)
            ),
            data={"name": "change"},
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_simple_user()}",  # noqa: E501
        )

        self.assertEqual(response.status_code, 403)

    def test_update_category_with_super_user(self):
        self.category = self.make_category()
        response = self.client.patch(
            reverse(
                "event:category-retrieve-update", args=(self.category.id,)
            ),
            data={"alt_text": "Change"},
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_super_user()}",  # noqa: E501
        )
        self.assertEqual(response.status_code, 200)

    def test_list_events_by_category(self):
        self.address = self.make_address_event()
        self.image = self.make_image()
        self.category = self.make_category()
        self.account = self.make_account_create_user(
            email="event@user.com", username="eventusername"
        )
        self.event = self.make_event(
            address=self.address, image=self.image, account=self.account
        )
        response = self.client.get(
            reverse("event:events-by-category", args=(self.category.id,))
        )
        self.assertEqual(response.status_code, 200)
