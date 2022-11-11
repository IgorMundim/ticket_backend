from django.urls import reverse
from rest_framework import test

from account.tests.test_account_base import AccountMixin


class AccountTestApiAddress(test.APITestCase, AccountMixin):
    def setUp(self) -> None:

        self.account = self.make_account_create_user()
        self.address = self.make_address(account=self.account)
        self.data = {
            "account": f"{self.account.id}",
            "telephone": "31-999999999",
            "zipcode": "31600000",
            "complement": "Apatamento",
            "city": "Belo Horizonte",
            "neighborhood": "Independência (Barreiro)",
            "number": "10",
            "street": "Avenida",
            "uf": "MG",
            "types": "1",
        }
        self.app()
        return super().setUp()

    def test_create_simple_address(self):
        response = self.client.post(
            reverse("account:address-list-create", args=(self.account.id,)),
            data=self.data,
            HTTP_AUTHORIZATION=(f"Bearer {self.get_login_jwt(self.account)}"),
        )
        self.assertEqual(response.status_code, 201)

    def test_create_simple_address_with_anonymous_user(self):
        response = self.client.post(
            reverse("account:address-list-create", args=(self.account.id,)),
            data=self.data,
        )
        self.assertEqual(response.status_code, 401)

    def test_create_simple_address_is_not_owner(self):
        response = self.client.post(
            reverse("account:address-list-create", args=(self.account.id,)),
            data=self.data,
            HTTP_AUTHORIZATION=(
                f"Bearer {self.get_jwt_acess_token_super_user()}"
            ),
        )
        self.assertEqual(response.status_code, 403)

    def test_list_simple_address(self):
        response = self.client.get(
            reverse("account:address-list-create", args=(self.address.id,)),
            HTTP_AUTHORIZATION=(f"Bearer {self.get_login_jwt(self.account)}"),
        )
        self.assertEqual(response.status_code, 200)

    def test_list_simple_address_with_anonymous_user(self):
        response = self.client.get(
            reverse("account:address-list-create", args=(self.address.id,)),
        )
        self.assertEqual(response.status_code, 401)

    def test_list_simple_address_is_not_owner(self):
        response = self.client.get(
            reverse("account:address-list-create", args=[self.address.id]),
            HTTP_AUTHORIZATION=(
                f"Bearer {self.get_jwt_acess_token_super_user()}"
            ),
        )
        self.assertEqual(response.status_code, 403)

    def test_retrieve_simple_address_with_anonymouse_user(self):
        response = self.client.get(
            reverse("account:address-retrieve-update", args=(self.address.id,))
        )
        self.assertEqual(response.status_code, 401)

    def test_retrieve_simple_address(self):
        response = self.client.get(
            reverse(
                "account:address-retrieve-update", args=(self.address.id,)
            ),
            HTTP_AUTHORIZATION=(f"Bearer {self.get_login_jwt(self.account)}"),
        )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_simple_address_is_not_owner(self):
        response = self.client.get(
            reverse(
                "account:address-retrieve-update", args=(self.address.id,)
            ),
            HTTP_AUTHORIZATION=(
                f"Bearer {self.get_jwt_acess_token_simple_user()}"
            ),
        )
        self.assertEqual(response.status_code, 403)

    def test_update_simple_address_with_anonymouse_user(self):
        response = self.client.patch(
            reverse(
                "account:address-retrieve-update", args=(self.account.id,)
            ),
            data={"last_name": "partialupdate"},
        )
        self.assertEqual(response.status_code, 401)

    def test_update_simple_address(self):
        response = self.client.patch(
            reverse(
                "account:address-retrieve-update", args=(self.account.id,)
            ),
            data={"last_name": "partialupdate"},
            HTTP_AUTHORIZATION=(f"Bearer {self.get_login_jwt(self.account)}"),
        )
        self.assertEqual(response.status_code, 200)

    def test_update_simple_address_is_not_owner(self):
        response = self.client.patch(
            reverse(
                "account:address-retrieve-update", args=(self.account.id,)
            ),
            data={"last_name": "partialupdate"},
            HTTP_AUTHORIZATION=(
                f"Bearer {self.get_jwt_acess_token_simple_user()}"
            ),
        )
        self.assertEqual(response.status_code, 403)
