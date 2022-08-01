import pytest
from core.event.models import (
    Batck,
    Category,
    Event,
    Image,
    Stock,
    Ticket,
    TicketLeasing,
)
from customer.models import Address, Telephone
from django.utils import timezone


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
def single_telephone(db):
    return Telephone.objects.create(
        code="999",
        telephone="default",
        type="1",
        description="default",
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
    return Batck.objects.create(
        event_id=single_event,
        sequence=1,
        batck_start_date=timezone.now(),
        batck_stop_date=timezone.now(),
        description="default",
        is_active=True,
    )


@pytest.fixture
def single_ticket_leasing_with_batck(db, single_batck_with_event):
    return TicketLeasing.objects.create(
        batck_id=single_batck_with_event,
        name="default",
        descroption="default",
        is_active=True,
        store_price=50.10,
        sale_price=40.10,
        student_price=25.10,
    )


@pytest.fixture
def single_stock_with_ticket_leasing(db, single_ticket_leasing_with_batck):
    return Stock.objects.create(
        ticket_leasing_id=single_ticket_leasing_with_batck,
        units=1,
        units_sold=1,
        last_checked=timezone.now(),
    )


@pytest.fixture
def single_ticket_with_request_ticket_leasing(
    db, single_request, single_ticket_leasing_with_batck
):
    return Ticket.objects.create(
        request_id=single_request,
        ticket_leasing_id=single_ticket_leasing_with_batck,
        code="default",
        is_student=False,
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
