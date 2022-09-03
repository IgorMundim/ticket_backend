

from datetime import datetime

from account.tests.test_account_base import AccountTestBase
from event.models import Batch
from event.tests.test_event_base import EventTestBase


class EventModelTeste(EventTestBase, AccountTestBase):
    def setUp(self) -> None:
        self.address = self.make_address()
        self.image = self.make_image()
        self.category = self.make_category()
        self.account = self.make_account_create_user(email="event@user.com",username="eventusername")
        self.event = self.make_event(address=self.address, image=self.image, account=self.make_account_create_user())
        self.batch = self.make_batch(event=self.event)
        self.leasing = self.make_leasing(event=self.event)
        return super().setUp()


    def test_create_single_addrees(self):
        self.assertEqual(str(self.address),("%s - %s" % (self.address.city, self.address.uf)))


    def test_create_single_image(self):
        self.assertEqual(str(self.image),("%s" % (self.image.image_url)))
    
    
    def test_create_single_category(self):
        self.assertEqual(str(self.category), self.category.name)


    def test_create_event(self):
        self.assertEqual(str(self.event),self.event.name)
    

    def test_create_single_batch(self):
        self.assertEqual(str(self.batch), self.batch.description)
        self.assertEqual(Batch.objects.filter_by_saler(
            event_pk=1, 
            sales_qtd=0,
            batch_stop_date="2022-12-10"
            ), self.batch
        )
        self.assertEqual(Batch.objects.is_valid_change(
            id=0,
            sales_qtd=2,
            batch_stop_date=datetime.strptime('28 11 2022 09:59:34 +0000 (UTC)',
                      "%d %m %Y %H:%M:%S %z (%Z)"),
            event_pk=1,
        ), False)
        self.assertEqual(Batch.objects.is_valid_change(
            id=2,
            sales_qtd=-1,
            batch_stop_date=datetime.strptime('15 12 2022 09:59:34 +0000 (UTC)',
                      "%d %m %Y %H:%M:%S %z (%Z)"),
            event_pk=1,
        ), False)
        self.assertEqual(Batch.objects.is_valid_change(
            id=2,
            sales_qtd=10,
            batch_stop_date=datetime.strptime('15 12 2022 09:59:34 +0000 (UTC)',
                      "%d %m %Y %H:%M:%S %z (%Z)"),
            event_pk=1,
        ), True)
    def test_create_single_leasing(self):
        self.assertEqual(str(self.leasing), self.leasing.name)