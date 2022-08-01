from customer.models import Account, Customer, Producer, Request


def test_create_single_account(super_account):
    new_account = super_account
    get_account = Account.objects.all().first()
    assert new_account.id == get_account.id


def test_create_producer_account(single_producer):
    new_producer = single_producer
    get_producer = Producer.objects.all().first()
    assert new_producer.id == get_producer.id
    assert new_producer.account_id.is_staff == get_producer.account_id.is_staff

def test_create_customer_account(single_customer):
    new_customer = single_customer
    get_customer = Customer.objects.all().first()
    assert new_customer.id == get_customer.id

def test_create_request(single_request):
    new_request = single_request
    get_request = Request.objects.all().first()
    assert new_request.id == get_request.id
    assert new_request.customer_id.first_name == get_request.customer_id.first_name
