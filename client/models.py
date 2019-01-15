from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.utils import timezone
import random


class City(models.Model):
    postal_code = models.CharField(max_length=6, validators=[RegexValidator(
        regex='^\d{2}-{1}\d{3}$', message='Niewlasciwy kod pocztowy! Uzyj formatu XX-XXX.', code='nomatch')])
    city = models.CharField(max_length=32)

    def __str__(self):
        return self.postal_code + " " + self.city


class Address(models.Model):
    street = models.CharField(max_length=64)
    house_nr = models.IntegerField()
    apartment_nr = models.IntegerField(null=True, blank=True)
    city = models.ForeignKey(City, on_delete=models.PROTECT)

    def __str__(self):
        return self.city.postal_code + " " + self.street + " " + str(self.house_nr) + " " + str(self.apartment_nr)


class Creditworthiness(models.Model):
    JOBE_TYPE_CW = [('Umowa o prace na czas nieokreslony', 'Umowa o prace na czas nieokreslony'),
                    ('Umowa o prace na czas okreslony',
                     'Umowa o prace na czas okreslony'),
                    ('Umowa o dzielo', 'Umowa o dzielo'),
                    ('Umowa Zlecenie', 'Umowa Zlecenie'),
                    ('Umowa Agencyjna', 'Umowa Agencyjna')]
    earnings_per_month = models.IntegerField(blank=True, null=True)
    contract_type = models.CharField(
        blank=True, null=True, max_length=35, choices=JOBE_TYPE_CW)
    working_time = models.IntegerField(blank=True, null=True)


class CustomUser(AbstractUser):
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    pesel = models.CharField(max_length=11, unique=True, validators=[RegexValidator(
        regex='^\d{11}$', message='Niewlasciwy PESEL!', code='nomatch')])
    mothers_maiden_name = models.CharField(max_length=32, blank=True, validators=[RegexValidator(
        regex='^[a-zA-Z-]*$', message='Niewlasciwe nazwisko!', code='nomatch')])
    birth_day = models.DateTimeField(help_text="Data w formacie dd/mm/yyyy")
    telephone = models.CharField(max_length=9, unique=True, validators=[RegexValidator(
        regex='^\d{9}$', message='Niewlasciwy numer telefonu', code='nomatch')])
    creditworthiness = models.ForeignKey(
        Creditworthiness, on_delete=models.PROTECT, blank=True, null=True)

    REQUIRED_FIELDS = ['email', 'first_name',
                       'last_name', 'pesel', 'birth_day', 'telephone', 'address']
    USERNAME_FIELD = 'username'

    def __str__(self):
        return self.username


class Account(models.Model):
    CURRENCIES_CHOICE = [
        ('EUR', 'EUR'),
        ('PLN', 'PLN'),
        ('USD', 'USD'),
        ('JPY', 'JPY'),
        ('GBP', 'GBP'),
        ('CHF', 'CHF'),
        ('SAR', 'SAR'),
        ('RUB', 'RUB'),
        ('KRW', 'KRW')
    ]

    account_number = models.CharField(max_length=26, unique=True, validators=[
        RegexValidator(regex='^\d{26}$', message='Bledny numer rachunku', code='nomatch')])
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    balance = models.DecimalField(default=0, max_digits=10, decimal_places=2)
    transaction_limit = models.CharField(default='50', max_length=5, validators=[RegexValidator(
        regex='^[0-9]$', message='Bledny limit transakcji', code='nomatch')])
    currency = models.CharField(
        default='PLN', max_length=3, choices=CURRENCIES_CHOICE)
    is_active = models.CharField(default='1', max_length=1, validators=[RegexValidator(
        regex='^[0-1]{1}$', message='Bledna wartosc', code='nomatch')])
    creation_date = models.DateTimeField(default=timezone.now)
    account_type = models.CharField(max_length=1, validators=[RegexValidator(
        regex='^[0-2]{1}$', message='Bledna wartosc', code='nomatch')])


class Card(models.Model):

    def rand_cvv():
        cvv = str(random.randint(0, 10))
        cvv += str(random.randint(0, 10))
        cvv += str(random.randint(0, 10))
        return cvv

    def rand_card_number():
        card_nr = str(random.randint(0, 10))
        for i in range(15):
            card_nr += str(random.randint(0, 10))
        return card_nr

    CARD_CHOICES = [
        ('True', 'True'),
        ('False', 'False')
    ]

    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    card_number = models.CharField(default=rand_card_number, max_length=16, validators=[RegexValidator(
        regex='\d{16}', message='Numer karty powinien skladac sie tylko i wylacznie z 16 cyfr', code='nomatch'
    )])
    cvv = models.CharField(default=rand_cvv, max_length=3, validators=[RegexValidator(
        regex='\d{3}', message='Number CVV sklada sie z 3 cyfr', code='nomatch'
    )])
    is_nfc = models.CharField(
        default='False', max_length=5, choices=CARD_CHOICES)
    is_active = models.CharField(default='1', max_length=1, validators=[RegexValidator(
        regex='[0,1]{1}', message='Karta musi byc w jednym z dwoch stanow: 1(aktywna) 0(nieaktywan', code='nomatch'
    )])
    transaction_limit = models.CharField(default='50', max_length=5, validators=[RegexValidator(
        regex='[0-9]{1,5}'
    )])


class TransactionHistory(models.Model):
    source_bank_account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name='source_bank_account')
    destination_bank_account = models.ForeignKey(
        Account, on_delete=models.PROTECT, related_name='destination_bank_account')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    title = models.CharField(max_length=20)
    send_date = models.DateTimeField(default=timezone.now)


class Request(models.Model):
    worker_data = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, null=True, blank=True, related_name='worker_data')
    client_data = models.ForeignKey(
        CustomUser, on_delete=models.PROTECT, related_name='client_data')
    request_text = models.TextField()
    send_date = models.DateTimeField(default=timezone.now)
    is_verified = models.CharField(max_length=1, default='0', validators=[RegexValidator(
        regex='[0,1]', message='1 dla zweryfikowanego wniosku, 0 dla niezweryfikowanego'
    )])
    request_type = models.CharField(max_length=1, default='0', validators=[RegexValidator(
        regex='[0,1]', message='0 bez kategorii, 1 wniosek o kredyt, 2 wniosek o karte kredytowa'
    )])


class SavingAccount(models.Model):
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    interest = models.DecimalField(max_digits=2, decimal_places=2)
    period = models.CharField(max_length=3, validators=[RegexValidator(
        regex='^\d{0,3}$', message='Bledny okres', code='nomatch')])


class CreditAccount(models.Model):
    account_number = models.ForeignKey(Account, on_delete=models.CASCADE)
    interest = models.DecimalField(max_digits=2, decimal_places=2)
    credit_limit = models.CharField(max_length=7, validators=[RegexValidator(
        regex='^\d{0,7}$', message='Bledna wartosc', code='nomatch')])
