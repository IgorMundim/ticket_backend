from account.models import Account, Address, Customer, Producer
from django.test import TestCase


class AccountMixin:
    def make_account_create_user(
        self,
        username="user",
        email="user@user.com",
        password="@Abc12345",
        profile_image="",
    ):
        return Account.objects.create_user(
            email=email,
            username=username,
            password=password,
            profile_image=profile_image,
        )

    def make_account_super_user(
        self,
        username="superuser",
        email="superuser@user.com",
        password="@Abc12345",
    ):
        return Account.objects.create_superuser(
            email=email,
            username=username,
            password=password,
        )

    def make_address(
        self,
        account=None,
        telephone="31-999999999",
        zipcode="31600000",
        complement="Apatamento",
        city="Belo Horizonte",
        neighborhood="Independência (Barreiro)",
        number="10",
        street="30672772",
        uf="MG",
        types="1",
    ):
        return Address.objects.create(
            account=account,
            telephone=telephone,
            zipcode=zipcode,
            complement=complement,
            city=city,
            neighborhood=neighborhood,
            number=number,
            street=street,
            uf=uf,
            types=types,
        )

    def make_producer(
        self,
        account=None,
        business_name="Abc Ltda",
        cnpj="17938875100250",
        fantasy_name="Abc",
        state_registration="145526",
        municype_registration="4578953",
    ):
        return Producer.objects.create(
            account=account,
            business_name=business_name,
            cnpj=cnpj,
            fantasy_name=fantasy_name,
            state_registration=state_registration,
            municype_registration=municype_registration,
        )
    def make_customer(
        self,
        account=None,
        first_name="Aline",
        last_name="Martins",
        cpf="57455610225",
        britday="2000-01-01",
    ):
        return Customer.objects.create(
            account=account,
            first_name=first_name,
            last_name=last_name,
            cpf=cpf,
            britday=britday,
        )


class AccountTestBase(TestCase, AccountMixin):
    def setUp(self) -> None:
        return super().setUp()
