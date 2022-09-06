from account.tests.test_account_base import AccountMixin
from django.urls import reverse
from event.tests.test_event_base import EventMixin
from rest_framework import test


class EventApiv1TestBatch(test.APITestCase, EventMixin, AccountMixin):
    def setUp(self) -> None:
        self.make_image()
        self.account = self.make_account_create_user(
            email="event@user.com", username="eventusername"
        )        
        self.make_event_two(self.account)
        self.event_active = self.make_event(self.account)
        self.batch = self.make_batch(event=self.event_active)
        self.batch_two = self.make_batch(
            event=self.event_active,
            percentage="8.0",
            sales_qtd="5",
            batch_stop_date="2022-12-15",
            description="batch two",
            is_active=True,
            )

        self.data = {
            "event": f"{self.event_active.id}",
            "percentage": "10.0",
            "sales_qtd": "10",
            "batch_stop_date": "2022-12-20",
            "description": "batch three",
            "is_active": "true"
        }
        return super().setUp()

    def test_batch_list(self):
        response = self.client.get(
            reverse(
                "event:batch-list-create",
                args=(self.event_active.id,)
            )
        )
        self.assertEqual(response.status_code, 200)
    
    def test_batch_create_with_anonymouse_user(self):
        response = self.client.post(
            reverse(
                "event:batch-list-create",
                args=(self.event_active.id,)
            ),
            data=self.data,
        )
        self.assertEqual(response.status_code, 401)

    def test_batch_create_with_owner_user(self):
        response = self.client.post(
            reverse(
                "event:batch-list-create",
                args=(self.event_active.id,)
            ),
            data=self.data,
            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )
        self.assertEqual(response.status_code, 201)

    def test_batch_create_with_owner_user_and_conflicting_data(self):
        response = self.client.post(
            reverse(
                "event:batch-list-create",
                args=(self.event_active.id,)
            ),
            data={
                "event": f"{self.event_active.id}",
                "percentage": "5.0",
                "sales_qtd": "0",
                "batch_stop_date": "2022-12-10",
                "description": "batch two",
                "is_active": "true"
            },
            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )
        self.assertEqual(response.status_code, 400)

    def test_batch_create_is_not_owner(self):
        response = self.client.post(
            reverse(
                "event:batch-list-create",
                args=(self.event_active.id,)
            ),
            data=self.data,
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_super_user()}",  # noqa: E501
        )
        self.assertEqual(response.status_code, 403)

    def test_batch_retrieve_with_anonymouse_user(self):
        response = self.client.get(
            reverse("event:batch-retrieve-update", args=(self.batch.id,))
        )
        self.assertEqual(response.status_code, 200)

    def test_batch_update_with_owner_user_when_patch(self):
        response = self.client.patch(
            reverse(
                "event:batch-retrieve-update", args=(self.batch.id,),
            ),
            data={"is_active": "false"},
            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )

        self.assertEqual(response.status_code, 400)
    
    def test_batch_update_with_owner_user_and_conflicting_data(self):
        response = self.client.put(
            reverse(
                "event:batch-retrieve-update",
                args=(self.batch_two.id,)
            ),
            data={
                "event": f"{self.event_active.id}",
                "percentage": "5.0",
                "sales_qtd": "0",
                "batch_stop_date": "2022-12-10",
                "description": "batch two",
                "is_active": "true"
            },
            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )
        self.assertEqual(response.status_code, 400)

    def test_batch_update_with_owner_user(self):
        response = self.client.put(
            reverse(
                "event:batch-retrieve-update",
                args=(self.batch_two.id,)
            ),
            data={
                "event": f"{self.event_active.id}",
                "percentage": "5.0",
                "sales_qtd": "10",
                "batch_stop_date": "2022-12-15",
                "description": "batch two",
                "is_active": "true"
            },
            HTTP_AUTHORIZATION=f"Bearer {self.get_login_jwt(self.account)}",
        )
        self.assertEqual(response.status_code, 200)
    
    def test_batch_update_is_not_owner(self):
        response = self.client.put(
            reverse(
                "event:batch-retrieve-update", args=(self.batch.id,),
            ),
            data={"is_active": "false", "event": f"{self.event_active.id}"},
            HTTP_AUTHORIZATION=f"Bearer {self.get_jwt_acess_token_super_user()}",  #noqa E501
        )

        self.assertEqual(response.status_code, 403)
