import pytest
from django.utils import timezone

from account.models import Address
from event.models import (Batch, Category, Event, Image)


@pytest.fixture
def create_address_account(db, single_account):
    return Address.objects.create(
        account_id=single_account,
        cep="default",
        complement="default",
        city="default",
        district="default",
        municipality_IBGE="10",
        number="10",
        roud="default",
        state="default",
        uf="MG",
        uf_ibge="1",
        types="1",
    )



@pytest.fixture
def single_address(db):
    return Address.objects.create(
        cep="default",
        complement="default",
        city="default",
        district="default",
        municipality_IBGE="10",
        number="10",
        roud="default",
        state="default",
        uf="MG",
        uf_ibge="1",
        types="1",
    )


@pytest.fixture
def single_event(db, single_producer, single_address, single_telephone):
    return Event.objects.create(
        producer_id=single_producer,
        address_id=single_address,
        telephone_id=single_telephone,
        name="default",
        in_room=True,
        date_end=timezone.now(),
        date_start=timezone.now(),
        description="default",
        is_virtual=False,
        video_url="default.url",
    )


@pytest.fixture
def single_image_with_event(db, single_event):
    return Image.objects.create(
        event_id=single_event,
        image_url="default.png",
        alt_text="default",
    )


@pytest.fixture
def single_batck_with_event(db, single_event):
    return Batch.objects.create(
        event_id=single_event,
        sequence=1,
        batck_start_date=timezone.now(),
        batck_stop_date=timezone.now(),
        description="default",
        is_active=True,
    )



@pytest.fixture
def single_category(db):
    return Category.objects.create(
        name="default",
        slug="defaut-slug",
        is_active=True,
    )


@pytest.fixture
def category_with_child(db):
    parent = Category.objects.create(
        name="default",
        slug="defaut",
        is_active=True,
    )
    parent.children.create(
        name="child",
        slug="child",
        is_active=True,
    )
    child = parent.children.first()
    return child


@pytest.fixture
def category_event(db, single_category, single_event):
    category = single_category
    category.events.add(single_event)
    return category
