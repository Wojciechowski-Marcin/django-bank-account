from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator


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


class CustomUser(AbstractUser):
    first_name = models.CharField(max_length=30, verbose_name='first name'),
    last_name = models.CharField(max_length=150, verbose_name='last name'),
    address = models.ForeignKey(Address, on_delete=models.PROTECT)
    pesel = models.CharField(max_length=11, unique=True, validators=[RegexValidator(
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


"""
class Creditworthiness:
    earnings =
    contract_type =
    working_time =
"""
