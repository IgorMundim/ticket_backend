# Create your models here.
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from django.utils import timezone
from utils.validation import strong_password


class AccountManage(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(
        self, email, username, password, profile_image, **other_fields
    ):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")
        email = self.normalize_email(email)
        user = self.model(
            email=email,
            username=username,
            profile_image=profile_image,
            **other_fields
        )
        strong_password(password)

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password, **other_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        other_fields.setdefault("is_staff", True)
        other_fields.setdefault("is_superuser", True)
        other_fields.setdefault("is_active", True)
        other_fields.setdefault("is_admin", True)

        if other_fields.get("is_staff") is not True:
            raise ValueError("Superuser must be assigned to is_staff=True.")
        if other_fields.get("is_superuser") is not True:
            raise ValueError(
                "Superuser must be assigned to is_superuser=True."
            )

        return self.create_user(email, username, password, "", **other_fields)


class Account(AbstractBaseUser, PermissionsMixin):
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    username = models.CharField(max_length=60, unique=True)
    email = models.CharField(max_length=60, unique=True)
    profile_image = models.ImageField(
        upload_to="account/covers/%Y/%m/%d/", blank=True, default=""
    )
    hide_email = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = AccountManage()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["email"]
        verbose_name = "account"
        verbose_name_plural = "account"


class Address(models.Model):
    account = models.ForeignKey(Account, on_delete=models.CASCADE, blank=True)
    telephone = models.CharField(max_length=20, default="")
    zipcode = models.CharField(max_length=8)
    complement = models.CharField(max_length=150, default="")
    city = models.CharField(max_length=100, default="")
    neighborhood = models.CharField(max_length=100)
    number = models.IntegerField()
    street = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    types = models.IntegerField()

    def __str__(self):
        return "%s - %s" % (self.city, self.uf)

    class Meta:
        verbose_name = "address"
        verbose_name_plural = "addresses"


class Producer(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    business_name = models.CharField(
        verbose_name="business name", max_length=100
    )
    cnpj = models.CharField(max_length=14)
    fantasy_name = models.CharField(verbose_name="fantasy name", max_length=45)
    state_registration = models.CharField(
        verbose_name="state registration", max_length=45
    )
    municype_registration = models.CharField(
        verbose_name="municype registration", max_length=45
    )

    def __str__(self):
        return self.business_name

    class Meta:
        verbose_name = "producer"
        verbose_name_plural = "producers"


class Customer(models.Model):
    account = models.OneToOneField(Account, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name="first name", max_length=100)
    last_name = models.CharField(verbose_name="last name", max_length=100)
    cpf = models.CharField(max_length=8)
    britday = models.DateField()

    def __str__(self):
        return "%s %s" % (self.first_name, self.last_name)

    class Meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"
