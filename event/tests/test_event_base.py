from django.test import TestCase
from django.utils import timezone


from event.models import Address, Batch, Category, Event, Image, Leasing

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
            date_end="2022-12-01",
            date_start="2022-12-28",
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
    def make_batch(
        self,
        event=None,
        percentage="5.0",
        sales_qtd="0",
        batch_stop_date="2022-12-10",
        description="batch start",
        is_active=True,
        ):
            return Batch.objects.create(
                event=event,
                percentage=percentage,
                sales_qtd=sales_qtd,
                batch_stop_date=batch_stop_date,
                description=description,
                is_active=is_active,
            )
    def make_leasing(
        self,
        event=None,
        name="Bloco A",
        descroption="Proximo ao balhero",
        is_active=True,
        store_price="100.00",
        sale_price="110.00",
        student_price="60.00",
        units_solid=0,
        units=10,
    ):
        return Leasing.objects.create(    
            event=event,
            name=name,
            descroption=descroption,
            is_active=is_active,
            store_price=store_price,
            sale_price=sale_price,
            student_price=student_price,
            units_solid=units_solid,
            units=units,
        )

class EventTestBase(TestCase,EventMixin):
    def setUp(self) -> None:
        return super().setUp()