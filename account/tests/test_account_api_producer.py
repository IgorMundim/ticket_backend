
from account.tests.test_account_base import AccountMixin
from rest_framework import test
from django.urls import reverse


class AccountTestApiProducer(test.APITestCase, AccountMixin):

    def setUp(self) -> None:
        self.account = self.make_account_create_user()
        self.account_two = self.make_account_create_user(
            username="user_two",
            email="user_two@user.com",
            password="@Abc12345",
            profile_image="",
        )
        self.producer = self.make_producer(account=self.account)
        self.data = {
            "account": f"{self.account_two.id}",
            "business_name": "Cba Ltda",
            "cnpj": "51965745144405",
            "fantasy_name": "Cba",
            "state_registration": "101578",
            "municype_registration": "1452526",
        }
        return super().setUp()
    
    def test_create_simple_producer(self):
        response = self.client.post(
            reverse("account:producer-create", args=(self.account_two.id,)),
            data=self.data,
            HTTP_AUTHORIZATION=(
                f"Bearer {self.get_login_jwt(self.account_two)}"
            ), 
        )
        self.assertEqual(response.status_code, 201)

    def test_create_simple_producer_with_anonymous_user(self):
        response = self.client.post(
            reverse("account:producer-create", args=(self.account_two.id,)),
            data=self.data,
        )
        self.assertEqual(response.status_code, 401)

    def test_create_simple_producer_is_not_owner(self):
        response = self.client.post(
            reverse("account:producer-create", args=(self.account_two.id,)),
            data=self.data,
            HTTP_AUTHORIZATION=(
                f"Bearer {self.get_login_jwt(self.account)}"
            ), 
        )   
        self.assertEqual(response.status_code, 403)

    def test_retrieve_simple_producer_with_anonymouse_user(self):
        response = self.client.get(
            reverse(
                "account:producer-retrieve-update",
                args=(self.producer.id,)
            )
        )
        self.assertEqual(response.status_code, 401)

    def test_retrieve_simple_producer(self):
        response = self.client.get(
            reverse(
                "account:producer-retrieve-update",
                args=(self.producer.id,)
            ),
            HTTP_AUTHORIZATION=(
                f"Bearer {self.get_login_jwt(self.account)}"
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_retrieve_simple_producer_is_not_owner(self):
        response = self.client.get(
            reverse(
                "account:producer-retrieve-update",
                args=(self.producer.id,)
            ),
            HTTP_AUTHORIZATION=(
                f"Bearer {self.get_jwt_acess_token_simple_user()}"
            )
        )
        self.assertEqual(response.status_code, 403)

    def test_update_simple_producer_with_anonymouse_user(self):
        response = self.client.patch(
            reverse(
                "account:producer-retrieve-update", args=(self.account.id,)
            ),
            data={"fantasy_name": "partialupdate"},
        )
        self.assertEqual(response.status_code, 401) 

    def test_update_simple_producer(self):
        response = self.client.patch(
            reverse(
                "account:producer-retrieve-update", args=(self.account.id,)
            ),
            data={"fantasy_name": "partialupdate"},
            HTTP_AUTHORIZATION=(
                f"Bearer {self.get_login_jwt(self.account)}"
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_update_simple_producer_is_not_owner(self):
        response = self.client.patch(
            reverse(
                "account:producer-retrieve-update", args=(self.account.id,)
            ),
            data={"fantasy_name": "partialupdate"},
            HTTP_AUTHORIZATION=(
                f"Bearer {self.get_jwt_acess_token_simple_user()}"
            )
        )
        self.assertEqual(response.status_code, 403)