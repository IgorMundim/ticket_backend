from account.models import Account
from account.tests.test_account_base import AccountTestBase
from django.core.exceptions import ValidationError


class AccountModelTest(AccountTestBase):
    def setUp(self) -> None:
        self.account_create_user = self.make_account_create_user()
        self.account_super_user = self.make_account_super_user()
        self.address = self.make_address(account=self.account_create_user)
        self.producer = self.make_producer(account=self.account_create_user)
        self.customer = self.make_customer(account=self.account_create_user)


        return super().setUp()

    def test_create_single_user(self):
        self.assertEqual(
            str(self.account_create_user), self.account_create_user.username
        )
        self.assertFalse(self.account_create_user.is_staff)
        self.assertFalse(self.account_create_user.is_superuser)
        self.assertFalse(self.account_create_user.is_admin)
        self.assertTrue(self.account_create_user.is_active)

    def test_create_super_user(self):
        self.assertTrue(self.account_super_user.is_staff)
        self.assertTrue(self.account_super_user.is_superuser)
        self.assertTrue(self.account_super_user.is_admin)
        self.assertTrue(self.account_super_user.is_active)

    def test_create_account_user_with_values_false(self):
        with self.assertRaises(ValueError):
            Account.objects.create_user(
                username="supererror", 
                email=None, 
                password="@Abc12345", 
                profile_image="",
            )
        with self.assertRaises(ValueError):
            Account.objects.create_user(
                username=None, 
                email="usernamefalse@user.com",
                password="@Abc12345", 
                profile_image="",
            )

    def test_create_account_super_user_with_values_false(self):

        with self.assertRaises(ValueError):
            Account.objects.create_superuser(
                username="supererror", 
                email="supererror@user.com", 
                password="@Abc12345", 
                is_staff=False,
            )
        with self.assertRaises(ValueError):
            Account.objects.create_superuser(
                username="supererror", 
                email="supererror@user.com", 
                password="@Abc12345", 
                is_superuser=False,
            )
    def test_create_single_address(self):
        self.assertEqual(str(self.address), ("%s - %s" % (self.address.city, self.address.uf)))

    def test_create_single_producer(self):
        self.assertEqual(str(self.producer),self.producer.business_name)

    def test_create_single_customer(self):
        self.assertEqual(str(self.customer), ("%s %s" % (self.customer.first_name, self.customer.last_name)))
