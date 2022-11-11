from django.test import TestCase
from django.utils.timezone import now, timedelta
from oauth2_provider.models import (
    get_access_token_model,
    get_application_model,
)

from account.models import Account, Address, Customer, Producer

ApplicationModel = get_application_model()
AccessTokenModel = get_access_token_model()


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

    def get_jwt_acess_token_super_user(self):
        userdata = {
            "username": "username",
            "password": "@Abc12345",
            "email": "superusercheck@user.com",
        }

        account = self.make_account_super_user(
            username=userdata.get("username"),
            password=userdata.get("password"),
            email=userdata.get("email"),
        )

        token = AccessTokenModel.objects.create(
            user=account,
            token="fgsfdtokstrsuper",
            application=self.app,
            expires=now() + timedelta(days=365),
        )
        return token

    def get_jwt_acess_token_simple_user(self):
        userdata = {
            "username": "simpleuser",
            "password": "@Abc12345",
            "email": "simpleuser@user.com",
        }

        account = self.make_account_create_user(
            username=userdata.get("username"),
            password=userdata.get("password"),
            email=userdata.get("email"),
        )
        token = AccessTokenModel.objects.create(
            user=account,
            token="tokstr",
            application=self.app,
            expires=now() + timedelta(days=365),
        )
        return token

    def get_login_jwt(self, account):
        token = AccessTokenModel.objects.create(
            user=account,
            token="tokstr",
            application=self.app,
            expires=now() + timedelta(days=365),
        )
        return token

    def app(self):
        superUser = self.make_account_super_user(
            username="superuseradm",
            email="superuseradm@user.com",
            password="@Abc12345",
        )

        self.app = ApplicationModel.objects.create(
            name="app",
            client_type=ApplicationModel.CLIENT_CONFIDENTIAL,
            authorization_grant_type=ApplicationModel.GRANT_CLIENT_CREDENTIALS,
            user=superUser,
        )


class AccountTestBase(TestCase, AccountMixin):
    def setUp(self) -> None:

        return super().setUp()
