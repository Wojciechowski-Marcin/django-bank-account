from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone

class City(models.Model):
    postal_code = models.CharField(max_length=6, primary_key=True, validators=[RegexValidator(
        regex='^\d{2}-{1}\d{3}$', message='Niewlasciwy kod pocztowy! Uzyj formatu XX-XXX.', code='nomatch')])
    city = models.CharField(max_length=32)

    def __str__(self):
        return self.postal_code + " " + self.city


class Address(models.Model):
    street = models.CharField(max_length=64)
    house_nr = models.IntegerField()
    apartment_nr = models.IntegerField(null=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    def __str__(self):
        return self.city.postal_code + " " + self.street + " " + str(self.house_nr) + " " + str(self.apartment_nr)


class CustomUser(AbstractUser):
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    pesel = models.CharField(max_length=11, validators=[RegexValidator(
        regex='^\d{11}$', message='Niewlasciwy PESEL!', code='nomatch')])
    mothers_maiden_name = models.CharField(max_length=32, blank=True, validators=[RegexValidator(
        regex='^[a-zA-Z-]*$', message='Niewlasciwe nazwisko!', code='nomatch')])
    birth_day = models.DateTimeField(help_text="Data w formacie dd/mm/yyyy")
    telephone = models.CharField(max_length=9, unique=True, validators=[RegexValidator(
        regex='^\d{9}$', message='Niewlasciwy numer telefonu', code='nomatch')])

    REQUIRED_FIELDS = ['email', 'first_name',
                       'last_name', 'pesel', 'birth_day', 'telephone', 'address']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class BankAccount(models.Model):
    account_number = models.CharField(max_length=26, primary_key=True, validators=[RegexValidator(regex='^\d{26}$', message='Bledny numer rachunku', code='nomatch')])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_limit = models.CharField(max_length=5, validators=[RegexValidator(regex='^[0-9]$', message='Bledny limit transakcji', code='nomatch')])
    currency = models.CharField(max_length=3, validators=[RegexValidator(regex='^[A-Z]{3}$', message='Bledna waluta', code='nomatch')])
    is_active = models.CharField(max_length=1, validators=[RegexValidator(regex='^[0,1]{1}$', message='Bledna wartosc', code='nomatch')])
    creation_date = models.DateTimeField(default=timezone.now)
    account_type = models.CharField(max_length=1, validators=[RegexValidator(regex='^[0,1]{1}$', message='Bledna wartosc', code='nomatch')])

class SavingAccount(models.Model):
    saving_id = models.CharField(max_length=6, primary_key=True, validators=[RegexValidator(regex='^\d{6}$', message='Bledna wartosc', code='nomatch')])
    account_number = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    interest = models.DecimalField(max_digits=2, decimal_places=2)
    period = models.CharField(max_length=3, validators=[RegexValidator(regex='^\d{3}$', message='Bledny okres', code='nomatch')])

class CreditAccount(models.Model):
    credit_id = models.CharField(max_length=6, primary_key=True, validators=[RegexValidator(regex='^\d{6}$', message='Bledna wartosc', code='nomatch')])
    account_number = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    interest2 = models.DecimalField(max_digits=2, decimal_places=2)
    credit_limit = models.CharField(max_length=7, validators=[RegexValidator(regex='^\d{7}$', message='Bledna wartosc', code='nomatch')])




"""
class Creditworthiness:
    earnings =
    contract_type =
    working_time =
"""
