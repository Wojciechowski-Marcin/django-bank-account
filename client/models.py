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



class Creditworthiness(models.Model):
    worthiness_id = models.CharField(max_length=6, primary_key=True)
    earnings_per_month = models.IntegerField(max_length=6)
    contract_type = models.CharField(max_length=1, validators=[RegexValidator(
        regex='[0-5]', message='0 - umowa o pracę na czas nieokreślony \n 1 - umowa o pracę na czas określony \n 2 - umowa o pracę na okres próbny \n 3 - umowa o dzieło 4 - umowa zlecenie 5 - umowa agencyjna'
    )])
    working_time = models.IntegerField(max_length=3)

class Card(models.Model):
    account_number = models.ForeignKey(BankAccount, on_delete=models.PROTECT)
    card_number = models.CharField(max_length=16, primary_key=True, validators=[RegexValidator(
        regex='\d{16}', message='Numer karty powinien skladac sie tylko i wylacznie z 16 cyfr', code='nomatch'
    )])
    cvv = models.CharField(max_length=3, validators=[RegexValidator(
        regex='\d{3}', message='Number CVV sklada sie z 3 cyfr', code='nomatch'
    )])
    is_nfc = models.CharField(max_length=1, validators=[RegexValidator(
        regex='[0,1]{1}', message='Platnosc zblizeniowa musi byc w jednym z dwoch stanow: 1(aktywna) 0(nieaktywan', code='nomatch'
    )])
    is_active = models.CharField(max_length=1, validators=[RegexValidator(
        regex='[0,1]{1}', message='Karta musi byc w jednym z dwoch stanow: 1(aktywna) 0(nieaktywan', code='nomatch'
    )])
    transaction_limit = models.CharField(max_length=1, validators=[RegexValidator(
        regex='[0-9]{1,5}'
    )])

class TransactionHistory(models.Model):
    source_bank_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT)
    destination_bank_account = models.ForeignKey(BankAccount, on_delete=models.PROTECT)
    transaction_id = models.CharField(max_length=9, primary_key=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.CharField(max_length=20)
    send_date = models.DateTimeField(default=timezone.now)

class Request(models.Model):
    request_id = models.CharField(max_length=6, primary_key=True)
    worker_data = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    client_data = models.ForeignKey(CustomUser, on_delete=models.PROTECT)
    request_text = models.CharField(max_length=255)
    send_date = models.DateTimeField(default=timezone.now)
    is_verified = models.CharField(max_length=1, validators=[RegexValidator(
        regex='[0,1]', message = '1 dla zweryfikowanego wniosku, 0 dla niezweryfikowanego'
    )])
    request_type = models.CharField(max_length=1, validators=[RegexValidator(
        regex='[0,1]', message = '1 dla zweryfikowanego wniosku, 0 dla niezweryfikowanego'
    )])