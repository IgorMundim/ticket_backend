from django.urls import reverse
from rest_framework import test

from account.tests.test_account_base import AccountMixin
from event.tests.test_event_base import EventMixin


class EventApiv1TestAddress(test.APITestCase, EventMixin, AccountMixin):
    def setUp(self) -> None:
        self.make_image()
        self.account = self.make_account_create_user(
            email="event@user.com", username="eventusername"
        )
        self.make_event_two(self.account)
        self.event_active = self.make_event(self.account)
        self.data = {
            "zipcode": "31600000",
            "complement": "Apatamento",
            "city": "Belo Horizonte",
            "neighborhood": "Independência (Barreiro)",
            "number": "10",
            "street": "30672772",
            "uf": "MG",
        }
        self.app()
        return super().setUp()

    def test_address_list(self):
        response = self.client.get(
            reverse(
                "event:address-list-create",
                args=(self.event_active.id,),
            ),
        )
        self.assertEqual(response.status_code, 200)

    def test_address_create(self):
        response = self.client.post(
            reverse(
                "event:address-list-create",
                args=(self.event_active.id,),
            ),
            data=self.data,
            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )
        self.assertEqual(response.status_code, 201)

    def test_address_create_with_anonymous_user(self):
        response = self.client.post(
            reverse(
                "event:address-list-create",
                args=(self.event_active.id,),
            ),
            data=self.data,
        )
        self.assertEqual(response.status_code, 401)

    def test_address_create_is_not_owner(self):
        response = self.client.post(
            reverse(
                "event:address-list-create",
                args=(self.event_active.id,),
            ),
            data=self.data,
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_super_user()}",  # noqa: E501
        )
        self.assertEqual(response.status_code, 403)

    def test_address_update(self):
        response = self.client.patch(
            reverse(
                "event:address-retrieve-update-destroy",
                args=(2,),
            ),
            data={"number": "1"},
            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )
        self.assertEqual(response.status_code, 200)

    def test_address_update_with_anonymous_user(self):
        response = self.client.patch(
            reverse(
                "event:address-retrieve-update-destroy",
                args=(2,),
            ),
            data={"number": "1"},
        )
        self.assertEqual(response.status_code, 401)

    def test_address_update_is_not_owner(self):
        response = self.client.patch(
            reverse(
                "event:address-retrieve-update-destroy",
                args=(2,),
            ),
            data={"number": "1"},
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_super_user()}",  # noqa: E501
        )
        self.assertEqual(response.status_code, 403)

    def test_address_destroy(self):
        response = self.client.patch(
            reverse(
                "event:address-retrieve-update-destroy",
                args=(2,),
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )
        self.assertEqual(response.status_code, 200)

    def test_address_destroy_with_anonymous_user(self):
        response = self.client.patch(
            reverse(
                "event:address-retrieve-update-destroy",
                args=(2,),
            ),
        )
        self.assertEqual(response.status_code, 401)

    def test_address_destroy_is_not_owner(self):
        response = self.client.patch(
            reverse(
                "event:address-retrieve-update-destroy",
                args=(2,),
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_super_user()}",  # noqa: E501
        )
        self.assertEqual(response.status_code, 403)
