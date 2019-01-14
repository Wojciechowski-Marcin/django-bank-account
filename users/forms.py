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
        fields = ['request_text', 'request_type']


class CardForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['transaction_limit', 'is_nfc']


class CreditworthinessForm(forms.ModelForm):
    JOBE_TYPE_CW = [('uopnt', 'Umowa o prace na czas nieokreslony'),
                    ('uop', 'Umowa o prace na czas okreslony'),
                    ('uod', 'Umowa o dzielo'),
                    ('uz', 'Umowa Zlecenie'),
                    ('ua', 'Umowa Agencyjna')]
    contract_type = models.CharField(
        max_length=5,
        choices=JOBE_TYPE_CW,
        blank=True
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
        field = ['transaction_limit', 'currency']

class SavingAccountForm(forms.ModelForm):
    class Meta:
        model = SavingAccount
        fields = ['period']

class CreditAccount(model.Model):
    class Meta:
        model = CreditAccount
        fields = ['credit_limit']