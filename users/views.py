from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from client.models import City
from .forms import UserRegisterForm, CityForm, AddressForm


def register(request):
    if request.method == 'POST':
        formA = UserRegisterForm(request.POST)
        formB = CityForm(request.POST)
        formC = AddressForm(request.POST)
        post_code = request.POST.get('postal_code')
        city = City.objects.filter(postal_code=post_code).first()
        if formA.is_valid() and (formB.is_valid or city) and formC.is_valid():
            a = formA.save(commit=False)
            if not city:
                b = formB.save()
            c = formC.save(commit=False)
            c.city = city
            c.save()
            a.address = c
            a.save()
            username = formA.cleaned_data.get('username')
            messages.success(request, f'Stworzono konto {username}!')
            return redirect('home')
    else:
        formA = UserRegisterForm()
        formB = CityForm()
        formC = AddressForm()
    return render(request, 'users/register.html', {'formA': formA, 'formB': formB, 'formC': formC})


@login_required
def profile(request):
    return render(request, 'users/profile.html')
