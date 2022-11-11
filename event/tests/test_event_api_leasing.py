from django.urls import reverse
from rest_framework import test

from account.tests.test_account_base import AccountMixin
from event.tests.test_event_base import EventMixin


class EventApiv1TestLeasing(test.APITestCase, EventMixin, AccountMixin):
    def setUp(self) -> None:
        self.make_image()
        self.account = self.make_account_create_user(
            email="event@user.com", username="eventusername"
        )
        self.make_event_two(self.account)
        self.event_active = self.make_event(self.account)
        self.batch = self.make_batch(event=self.event_active)
        self.leasing = self.make_leasing(event=self.event_active)
        self.data = {
            "event": f"{self.event_active.id}",
            "name": "Proximo a sala 3",
            "descroption": "Não é permitido entrada de ...",
            "is_active": "true",
            "store_price": "100",
            "units": "1",
        }
        self.app()
        return super().setUp()

    def test_leasing_list(self):
        response = self.client.get(
            reverse(
                "event:leasing-list-create",
                args=(self.event_active.id,),
            ),
        )
        self.assertEqual(response.status_code, 200)

    def test_leasing_create(self):
        response = self.client.post(
            reverse(
                "event:leasing-list-create",
                args=(self.event_active.id,),
            ),
            data=self.data,
            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )
        self.assertEqual(response.status_code, 201)

    def test_leasing_create_with_anonymous_user(self):
        response = self.client.post(
            reverse(
                "event:leasing-list-create",
                args=(self.event_active.id,),
            ),
            data=self.data,
        )
        self.assertEqual(response.status_code, 401)

    def test_leasing_create_is_not_owner(self):
        response = self.client.post(
            reverse(
                "event:leasing-list-create",
                args=(self.event_active.id,),
            ),
            data=self.data,
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_super_user()}",  # noqa: E501
        )
        self.assertEqual(response.status_code, 403)

    def test_leasing_update(self):
        response = self.client.patch(
            reverse(
                "event:leasing-retrieve-update",
                args=(self.leasing.id,),
            ),
            data={"units": "1"},
            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )
        self.assertEqual(response.status_code, 200)

    def test_leasing_update_with_anonymous_user(self):
        response = self.client.patch(
            reverse(
                "event:leasing-retrieve-update",
                args=(self.leasing.id,),
            ),
            data={"units": "1"},
        )
        self.assertEqual(response.status_code, 401)

    def test_leasing_update_is_not_owner(self):
        response = self.client.patch(
            reverse(
                "event:leasing-retrieve-update",
                args=(self.leasing.id,),
            ),
            data={"units": "1"},
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_super_user()}",  # noqa: E501
        )
        self.assertEqual(response.status_code, 403)

    def test_leasing_update_with_units_invalid(self):
        response = self.client.patch(
            reverse(
                "event:leasing-retrieve-update",
                args=(self.leasing.id,),
            ),
            data={"units": "-1"},
            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )
        self.assertEqual(response.status_code, 400)
