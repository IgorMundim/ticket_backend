import io
from account.tests.test_account_base import AccountMixin
from rest_framework import test
from django.urls import reverse

from PIL import Image
import tempfile


def temporary_image():
    """
    Returns a new temporary image file
    """
    image = Image.new('RGB', (100, 100))
    tmp_file = tempfile.NamedTemporaryFile(suffix='.jpg')
    image.save(tmp_file, 'jpeg')
    tmp_file.seek(0)  
    return tmp_file


class AccountTestApi(test.APITestCase, AccountMixin):

    def setUp(self) -> None:
        self.account = self.make_account_create_user()
    
        self.data = {
            "username": "testapicreateuser",
            "email": "testapicreateuser@user.com",
            "password": "@Abc12345",
            "password2": "@Abc12345",
            "profile_image": temporary_image()
        }
        return super().setUp()
    
    def test_create_simple_account(self):
        response = self.client.post(
            reverse("account:account-create"),
            data=self.data,
            format="multipart"
        )
        self.assertEqual(response.status_code, 201)

    def test_create_simple_account_with_invalid_password(self):
        response = self.client.post(
            reverse("account:account-create"),
            data={
                "username": "test",
                "email": "test@user.com",
                "password": "12345",
                "password2": "12345",
                "profile_image": temporary_image()
            },
            format="multipart"
        )
        self.assertEqual(response.status_code, 400)

    def test_update_simple_account(self):
        response = self.client.patch(
            reverse(
                "account:account-retrieve-update", args=(self.account.id,)
            ),
            data={"username": "partialupdate"},
            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )
        self.assertEqual(response.status_code, 200)

    def test_update_simple_account_with_invalid_password(self):
        response = self.client.patch(
            reverse(
                "account:account-retrieve-update", args=(self.account.id,)
            ),
            data={"password": "@Abcd1234", "password2": "@Abc1234"},
            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )
        self.assertEqual(response.status_code, 400)   

    def test_update_simple_account_with_anonymouse_user(self):
        response = self.client.patch(
            reverse(
                "account:account-retrieve-update", args=(self.account.id,)
            ),
            data={"username": "partialupdate"},
        )
        self.assertEqual(response.status_code, 401) 

    def test_update_simple_account_is_not_owner(self):
        response = self.client.patch(
            reverse(
                "account:account-retrieve-update", args=(self.account.id,)
            ),
            data={"username": "partialupdate"},
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_super_user()}",  # noqa: E501
        )
        self.assertEqual(response.status_code, 403) 

    def test_retrieve_simple_account(self):
        response = self.client.get(
            reverse(
                "account:account-retrieve-update", args=(self.account.id,)
            ),

            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )
        self.assertEqual(response.status_code, 200)