from django.test import TestCase
from django.utils import timezone


from event.models import Address, Category, Event, Image

class EventMixin:
    def make_address(
        self,
        zipcode="31600000",
        complement="Apatamento",
        city="Belo Horizonte",
        neighborhood="Independência (Barreiro)",
        number="10",
        street="30672772",
        uf="MG",
    ):
        return Address.objects.create(
            zipcode=zipcode,
            complement=complement,
            city=city,
            neighborhood=neighborhood,
            number=number,
            street=street,
            uf=uf,
        )

    
    def make_image(self,image_url="image.png",alt_text="descrição"):
        return Image.objects.create(image_url=image_url,alt_text=alt_text)

    def make_category(
        self,
        name="Show",
        slug="show",
        is_active=True,
        image_url="image.png",
        alt_text="descrição",
    ):
        return Category.objects.create(
            name=name,
            slug=slug,
            is_active=is_active,
            image_url=image_url,
            alt_text=alt_text,
        )
    def make_event(
            self,
            account=None,
            address=None,
            image=None,
            name="Show beneficiente",
            in_room=True,
            date_end="2019-03-28 15:14:19",
            date_start="2019-03-28 15:14:19",
            description="descrição",
            is_virtual=False,
            video_url="www.you.com",
            is_published="True",
        ):
            return Event.objects.create(
                account=account,
                address=address,
                image=image,
                name=name,
                in_room=in_room,
                date_end=date_end,
                date_start=date_start,
                description=description,
                is_virtual=is_virtual,
                video_url=video_url,
                is_published=is_published,
            )

class EventTestBase(TestCase,EventMixin):
    def setUp(self) -> None:
        return super().setUp()