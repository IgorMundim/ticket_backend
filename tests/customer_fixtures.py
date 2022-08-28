import pytest

from account.models import (Account, Address, Customer, Producer, Request,
                            Telephone)


@pytest.fixture
def single_account(db):
    return Account.objects.create(
        username="defautsingle",
        email="defaut@single.br",
        profile_image="default.png",
        password="abcd@#1",
    )


@pytest.fixture
def super_account(db):
    return Account.objects.create(
        username="defautsuper",
        email="defaut@super.com",
        profile_image="default.png",
        password="abcd@#1",
        is_superuser=True,
        is_admin=True,
        is_staff=True,
        is_active=True,
    )


@pytest.fixture
def account_producer(db):
    return Account.objects.create(
        username="defautproducer",
        email="defaut@producer.com",
        profile_image="default.png",
        password="abcd@#1",
        is_superuser=False,
        is_admin=False,
        is_staff=True,
        is_active=True,
    )


@pytest.fixture
def account_customer(db):
    return Account.objects.create(
        username="defautcustomer",
        email="defaut@customer.com",
        profile_image="default.png",
        password="abcd@#1",
        is_superuser=False,
        is_admin=False,
        is_staff=False,
        is_active=True,
    )


@pytest.fixture
def single_producer(db, account_producer):
    return Producer.objects.create(
        account_id=account_producer,
        business_name="default",
        cnpj="default",
        fantasy_name="default",
        state_registration="default",
        municype_registration="default",
    )


@pytest.fixture
def single_request(db, single_customer):
    return Request.objects.create(
        customer_id=single_customer,
        is_paid=True,
        type_of_payment="2",
    )


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
def single_customer(db, account_customer):
    return Customer.objects.create(
        account_id=account_customer,
        first_name="default",
        last_name="default",
        cpf="default",
        britday="2000-03-03",
    )


@pytest.fixture
def telephone_wite_account(db, single_account):
    return Telephone.objects.create(
        account_id=single_account,
        code="999",
        telephone="default",
        type="1",
        description="default",
    )
