

from event.tests.test_event_base import EventTestBase


class EventModelTeste(EventTestBase):
    def setUp(self) -> None:
        self.address = self.make_address()
        self.image = self.make_image()
        self.category = self.make_category()
        self.event = self.make_event(address=self.address, image=self.image,)
        return super().setUp()


    def test_create_single_addrees(self):
        self.assertEqual(str(self.address),("%s - %s" % (self.address.city, self.address.uf)))


    def test_create_single_image(self):
        self.assertEqual(str(self.image),("%s" % (self.image.image_url)))
    
    
    def test_create_single_category(self):
        self.assertEqual(str(self.category), self.category.name)

    def test_create_event(self):
        self.assertEqual(str(self.event),self.event.name)
