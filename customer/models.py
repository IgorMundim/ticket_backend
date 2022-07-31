from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db import models


class AccountManage(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have a username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None):
        if not email:
            raise ValueError("User must have an email address")
        if not username:
            raise ValueError("User must have username")
        user = self.model(
            email=self.normalize_email(email),
            username=username,
            password=password,
        )
        user.is_admin = (True,)
        user.is_staff = (True,)
        user.is_superuser = (True,)
        user.save(using=self._db)
        return user


class Account(AbstractBaseUser):
    last_login = models.DateTimeField(verbose_name="last login", auto_now=True)
    username = models.CharField(max_length=60, unique=True)
    email = models.CharField(max_length=60, unique=True)
    date_joined = models.DateTimeField(auto_now_add=True, editable=False)
    profile_image = models.ImageField(
        upload_to='core/covers/%Y/%m/%d/', blank=True, default=""
    )
    hide_email = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    objects = AccountManage()

    def __str__(self):
        return self.username

    class Meta:
        ordering = ["email"]
        verbose_name = "account"
        verbose_name_plural = "account"



class Telephone(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    code = models.CharField(max_length=4)
    telephone = models.CharField(max_length=12)
    type = models.IntegerField(default=1)
    description = models.CharField(max_length=150, blank=True,default="",)

    def __str__(self):
        return "%s-%s" % (self.code, self.telephone)
    class Meta:
        verbose_name = "telephone"
        verbose_name_plural = "phones"



class Address(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE,null=True)
    cep = models.CharField(max_length=8)
    city = models.CharField(max_length=100)
    complement = models.CharField(max_length=150, blank=True, default="")
    district = models.CharField(max_length=100)
    municipality_IBGE = models.IntegerField()
    number = models.IntegerField()
    roud = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    uf = models.CharField(max_length=2)
    uf_ibge = models.IntegerField()
    type = models.IntegerField()

    def __str__(self):
        return "Address"
    class Meta:
        verbose_name = "address"
        verbose_name_plural = "Adresses"



class Producer(models.Model):
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
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
    account_id = models.ForeignKey(Account, on_delete=models.CASCADE)
    first_name = models.CharField(verbose_name="first name", max_length=100)
    last_name = models.CharField(verbose_name="last name", max_length=100)
    cpf = models.CharField(max_length=8)
    britday = models.DateField()

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = "customer"
        verbose_name_plural = "customers"



class Request(models.Model):
    customer_id = models.ForeignKey(Customer, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(
        verbose_name="date joined", auto_now_add=True, editable=False
    )
    status = models.BooleanField()
    type_of_payment = models.DecimalField(verbose_name="type of payment",max_digits=2,decimal_places=0)

    def __str__(self):
        return self.date_joined
    class Meta:
        verbose_name = "request"
        verbose_name_plural = "requests"

