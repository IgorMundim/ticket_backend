from cmath import sin

from event.models import (
    Batck,
    Category,
    Event,
    Image,
    Stock,
    Ticket,
    TicketLeasing,
)


def test_create_event_with_producer_address_telephone(single_event):
    new_event = single_event
    get_event = Event.objects.all().first()
    assert new_event.id == get_event.id
    assert new_event.address_id.cep == get_event.address_id.cep
    assert new_event.telephone_id.code == get_event.telephone_id.code
    assert new_event.producer_id.cnpj == get_event.producer_id.cnpj


def test_create_image_with_event(single_image_with_event):
    new_image = single_image_with_event
    get_image = Image.objects.all().first()
    assert new_image.id == get_image.id
    assert new_image.event_id.name == get_image.event_id.name


def test_create_batck_with_event(single_batck_with_event):
    new_batck = single_batck_with_event
    get_batck = Batck.objects.all().first()
    assert new_batck.id == get_batck.id
    assert new_batck.event_id.is_virtual == get_batck.event_id.is_virtual


def test_create_ticket_leasing_with_batck(single_ticket_leasing_with_batck):
    new_ticket_leasing = single_ticket_leasing_with_batck
    get_ticket_leasing = TicketLeasing.objects.all().first()
    assert new_ticket_leasing.id == get_ticket_leasing.id
    assert (
        new_ticket_leasing.batck_id.sequence
        == get_ticket_leasing.batck_id.sequence
    )


def test_create_stock_with_ticket_leasing(single_stock_with_ticket_leasing):
    new_stock = single_stock_with_ticket_leasing
    get_stock = Stock.objects.all().first()
    assert new_stock.id == get_stock.id
    assert new_stock.ticket_leasing_id.name == get_stock.ticket_leasing_id.name


def test_create_ticket_with_request_ticket_leasing(
    single_ticket_with_request_ticket_leasing,
):
    new_ticket = single_ticket_with_request_ticket_leasing
    get_ticket = Ticket.objects.all().first()
    assert new_ticket.id == get_ticket.id
    assert new_ticket.request_id.is_paid == get_ticket.request_id.is_paid
    assert (
        new_ticket.ticket_leasing_id.name == get_ticket.ticket_leasing_id.name
    )


def test_create_single_category(single_category):
    new_category = single_category
    get_category = Category.objects.all().first()
    assert new_category.id == get_category.id


# def test_create_category_with_child(category_with_child):
#     new_sub_category = category_with_child
#     get_category = Category.objects.all().first()
#     assert get_category.children.first().id == new_sub_category.id


def test_create_category_event(category_event):
    new_category = category_event
    event_count = Event.objects.filter(category__id=1).count()
    assert event_count == 1
