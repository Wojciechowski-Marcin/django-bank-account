from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from client.models import Account


@login_required
def home(request):
    accounts = Account.objects.filter(user=request.user)
    context = {
        'accounts': accounts
    }
    return render(request, 'client/home.html', context)


@login_required
def request(request):
    return render(request, 'client/request.html')


@login_required
def open_account(request):
    return render(request, 'client/open_account.html')


@login_required
def open_credit_account(request):
    return render(request, 'client/open_credit_account.html')


@login_required
def open_saving_account(request):
    return render(request, 'client/open_saving_account.html')


@login_required
def transaction_history(request, oid):
    account = Account.objects.filter(id=oid).first()
    context = {
        'account': account
    }
    return render(request, 'client/transaction_history.html', context)


@login_required
def order_card(request, oid):
    account = Account.objects.filter(id=oid).first()
    context = {
        'account': account
    }
    return render(request, 'client/order_card.html', context)


@login_required
def make_transaction(request, oid):
    account = Account.objects.filter(id=oid).first()
    context = {
        'account': account
    }
    return render(request, 'client/make_transaction.html', context)


@login_required
def account(request, oid):
    account = Account.objects.filter(id=oid).first()
    context = {
        'account': account
    }
    return render(request, 'client/account.html', context)
