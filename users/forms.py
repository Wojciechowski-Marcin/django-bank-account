from django import forms
from client.models import CustomUser, City, Address
from django.contrib.auth.forms import UserCreationForm
import datetime


class UserRegisterForm(UserCreationForm):
    email = forms.EmailField()
    birth_day = forms.DateField(
        widget=forms.widgets.DateInput(format="%d/%m/%Y"), help_text='Date in format dd/mm/yyyy')

    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'pesel', 'birth_day',
                  'username', 'email', 'password1', 'password2', 'telephone']


class CityForm(forms.ModelForm):
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
        fields = ['request_text']

class Card(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['cvv', 'transaction_limit', 'shipping_address']