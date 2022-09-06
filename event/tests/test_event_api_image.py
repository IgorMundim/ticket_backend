from account.tests.test_account_base import AccountMixin
from django.urls import reverse
from event.tests.test_event_base import EventMixin
from rest_framework import test

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


class EventApiv1Testimage(test.APITestCase, EventMixin, AccountMixin):
    def setUp(self) -> None:
        self.image = self.make_image()
        self.account = self.make_account_create_user(
            email="event@user.com", username="eventusername"
        )        
        self.make_event_two(self.account)
        self.event_active = self.make_event(self.account)
        self.data = {
            "image_url": temporary_image(),
            "alt_text": "descrição",
            "event": f"{self.event_active.id}"
        }
        return super().setUp()

    def test_image_list(self):
        response = self.client.get(
            reverse(
                "event:image-list-create",
                args=(self.event_active.id,),
            ),
        )
        self.assertEqual(response.status_code, 200)

    def test_image_create(self):
        response = self.client.post(
            reverse(
                "event:image-list-create",
                args=(self.event_active.id,),
            ),
            data=self.data,
            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )
        self.assertEqual(response.status_code, 201)

    def test_image_create_with_anonymous_user(self):
        response = self.client.post(
            reverse(
                "event:image-list-create",
                args=(self.event_active.id,),
            ),
            data=self.data,
        )
        self.assertEqual(response.status_code, 401)

    def test_image_create_is_not_owner(self):
        response = self.client.post(
            reverse(
                "event:image-list-create",
                args=(self.event_active.id,),
            ),
            data=self.data,
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_super_user()}",  # noqa: E501
        )
        self.assertEqual(response.status_code, 403)
    
    def test_image_update(self):
        response = self.client.patch(
            reverse(
                "event:image-retrieve-update-destroy",
                args=(self.event_active.image_id,),
            ),
            data={"alt_text": "nova descrição"},
            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )
        self.assertEqual(response.status_code, 200)
    
    def test_image_update_with_anonymous_user(self):
        response = self.client.patch(
            reverse(
                "event:image-retrieve-update-destroy",
                args=(self.event_active.image_id,),
            ),
            data={"alt_text": "nova descrição"},
        )
        self.assertEqual(response.status_code, 401)

    def test_image_update_is_not_owner(self):
        response = self.client.patch(
            reverse(
                "event:image-retrieve-update-destroy",
                args=(self.event_active.image_id,),
            ),
            data={"alt_text": "nova descrição"},
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_super_user()}",  # noqa: E501
        )
        self.assertEqual(response.status_code, 403)

    def test_image_destroy(self):
        response = self.client.patch(
            reverse(
                "event:image-retrieve-update-destroy",
                args=(self.event_active.image_id,),
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )
        self.assertEqual(response.status_code, 200)
    
    def test_image_destroy_with_anonymous_user(self):
        response = self.client.patch(
            reverse(
                "event:image-retrieve-update-destroy",
                args=(self.event_active.image_id,),
            ),
        )
        self.assertEqual(response.status_code, 401)

    def test_image_destroy_is_not_owner(self):
        response = self.client.patch(
            reverse(
                "event:image-retrieve-update-destroy",
                args=(self.event_active.image_id,),
            ),
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_super_user()}",  # noqa: E501
        )
        self.assertEqual(response.status_code, 403)