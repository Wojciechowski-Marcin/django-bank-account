from django import forms
from client.models import *
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import datetime


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    birth_day = forms.DateField(
        input_formats=["%d/%m/%Y"], help_text='Date in format dd/mm/yyyy')

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'pesel', 'birth_day',
                  'username', 'email', 'password1', 'password2', 'telephone']


class UserEditForm(UserChangeForm):
    email = forms.EmailField()
    password = None

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name',
                  'username', 'email', 'telephone']


class CityForm(forms.ModelForm):
    postal_code = forms.CharField(help_text='Postal code in format XX-XXX')

    class Meta:
        model = City
        fields = ['postal_code', 'city']


class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['street', 'house_nr', 'apartment_nr']


class RequestForm(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['request_text']


class CardForm(forms.ModelForm):
    CARD_CHOICES = [
        ('True', 'True'),
        ('False', 'False')
    ]
    is_nfc = models.CharField(
        max_length=5,
        choices=CARD_CHOICES,
        blank=True,
        verbose_name='Enable contactless payments?'
    )

    class Meta:
        model = Card
        fields = ['transaction_limit', 'is_nfc']

class EditCardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['transaction_limit', 'is_nfc', 'is_active']

class CreditworthinessForm(forms.ModelForm):
    JOBE_TYPE_CW = [('Umowa o prace na czas nieokreslony', 'Umowa o prace na czas nieokreslony'),
                    ('Umowa o prace na czas okreslony',
                     'Umowa o prace na czas okreslony'),
                    ('Umowa o dzielo', 'Umowa o dzielo'),
                    ('Umowa Zlecenie', 'Umowa Zlecenie'),
                    ('Umowa Agencyjna', 'Umowa Agencyjna')]
    contract_type = models.CharField(
        max_length=35,
        choices=JOBE_TYPE_CW,
        blank=True,
        verbose_name='Contract type'
    )

    class Meta:
        model = Creditworthiness
        fields = ['earnings_per_month', 'working_time', 'contract_type']


class TransactionHistoryForm(forms.ModelForm):
    class Meta:
        model = TransactionHistory
        fields = ['destination_bank_account', 'amount', 'title']


class AccountForm(forms.ModelForm):
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
    currency = models.CharField(
        max_length=3,
        choices=CURRENCIES_CHOICE,
        blank=True
    )

    class Meta:
        model = Account
        fields = ['transaction_limit', 'currency']

class AccountEditForm(forms.ModelForm):
    class Meta:
        model = Account
        fields = [
            'transaction_limit', 'is_active',
        ]

class SavingAccountForm(forms.ModelForm):
    class Meta:
        model = SavingAccount
        fields = ['period']


class CreditAccountForm(forms.ModelForm):
    class Meta:
        model = CreditAccount
        fields = ['credit_limit']
