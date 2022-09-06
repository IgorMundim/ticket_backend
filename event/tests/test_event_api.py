from django.urls import reverse
from rest_framework import test

from account.tests.test_account_base import AccountMixin
from event.tests.test_event_base import EventMixin


class EventApiv1Test(test.APITestCase, EventMixin, AccountMixin):

    def setUp(self) -> None:
        self.make_image()
        self.account = self.make_account_create_user(
            email="event@user.com", username="eventusername"
        )        

        self.make_event_two(self.account)
        self.event_active = self.make_event(self.account)
        self.event_data = {
            "account": "1",
            "name": "Event",
            "in_room": "true",
            "date_end": "2022-12-30T10:00:00.000Z",
            "date_start": "2022-12-01T10:00:00.000Z",
            "description": "New event",
            "is_virtual": "true",
            "video_url": "www.you.com",
            "is_published": "true",
        }
        return super().setUp()

    def test_event_list(self):
        response = self.client.get(reverse("event:event-list-create"))
        self.assertEqual(response.status_code, 200)

    def test_event_list_do_not_activate(self):
        response = self.client.get(reverse("event:event-list-create"))
        self.assertEqual(len(response.data), 1)

    def test_event_create_with_anonymous_user(self):
        
        response = self.client.post(
            reverse("event:event-list-create"),
            data=self.event_data,
        )
        self.assertEqual(response.status_code, 401)

    def test_event_create_with_super_user(self):
        response = self.client.post(
            reverse("event:event-list-create"),
            data=self.event_data,
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_super_user()}",  # noqa: E501
        )
        self.assertEqual(response.status_code, 201)

    def test_event_create_with_super_user_forcing_error_404(self):
        response = self.client.post(
            reverse("event:event-list-create"),
            data={},
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_super_user()}",  # noqa: E501
        )
        self.assertEqual(response.status_code, 400)

    def test_event_create_with_simple_user(self):
        response = self.client.post(
            reverse("event:event-list-create"),
            data=self.event_data,
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_simple_user()}",  # noqa: E501
        )
        self.assertEqual(response.status_code, 201)
    
    def test_event_retrive_with_anonymous_user(self):

        response = self.client.get(
            reverse(
                "event:event-retrieve-update",
                args=(self.event_active.id,)
            )
        )
        self.assertEqual(response.status_code, 200)

    def test_event_update_with_anonymous_user(self):

        response = self.client.patch(
            reverse(
                "event:event-retrieve-update",
                args=(self.event_active.id,),
            ),
            data={"name": "new name"}
        )
        self.assertEqual(response.status_code, 401)
    
    def test_event_update_with_owner_user(self):
        response = self.client.patch(
            reverse(
                "event:event-retrieve-update",
                args=(self.event_active.id,),
            ),
            data={"name": "new name"},
            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )
        self.assertEqual(response.status_code, 200)
    
    def test_event_update_is_not_owner(self):
        response = self.client.patch(
            reverse(
                "event:event-retrieve-update",
                args=(self.event_active.id,),
            ),
            data={"name": "new name"},
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_super_user()}",  # noqa: E501
        )
        self.assertEqual(response.status_code, 403)
