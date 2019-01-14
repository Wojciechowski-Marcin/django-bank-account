from django import forms
from client.models import CustomUser, City, Address
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
import datetime

JOBE_TYPE_CW = [ ('uopnt', 'Umowa o prace na czas nieokreslony'), 
                ('uop', 'Umowa o prace na czas okreslony'), 
                ('uod', 'Umowa o dzielo'),
                ('uz', 'Umowa Zlecenie'),
                ('ua', 'Umowa Agencyjna')]


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

class Request(forms.ModelForm):
    class Meta:
        model = Request
        fields = ['request_text', 'type']

class Card(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['cvv', 'transaction_limit', 'shipping_address']
        #zmiana

class Creditworthiness(forms.ModelForm):
    class Meta:
        model = Creditworthiness
        fields = ['earnings_pre_month', 'working_time', 'contract_type']
        contract_type = forms.CharField(label='Rodzaj umowy',
        widget = forms.Select(choices=JOBE_TYPE_CW))

class TransactionHistory(forms.ModelForm):
    class Meta:
        model = TransactionHistory
        fields = ['Destination', 'Amount', 'Title', 'Address']
    