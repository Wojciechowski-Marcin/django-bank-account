from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from client.models import *
from users.forms import *


@login_required
def home(request):
    accounts = Account.objects.filter(user=request.user)
    context = {
        'accounts': accounts
    }
    return render(request, 'client/home.html', context)


@login_required
def send_request(request):
    if request.method == 'POST':
        form = RequestForm(request.POST)
        if form.is_valid():
            requestform = form.save(commit=False)
            requestform.client_data = request.user
            requestform.save()
            messages.success(
                request, 'Request was successfully sent!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = RequestForm()
    return render(request, 'client/send_request.html', {'form': form})


@login_required
def open_account(request):
    if request.method == 'POST':
        form = AccountForm(request.POST)
        if form.is_valid():
            accountform = form.save(commit=False)
            accountform.transact
            accountform.save()
            messages.success(
                request, 'Request was successfully sent!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = RequestForm()
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
    transaction = TransactionHistory.objects.filter(
        destination_bank_account=account)
    transaction2 = TransactionHistory.objects.filter(
        source_bank_account=account)
    transactions = list(transaction) + list(transaction2)
    transactions.sort(key=lambda t: t.send_date)
    context = {
        'account': account,
        'transactions': transactions
    }
    return render(request, 'client/transaction_history.html', context)


@login_required
def order_card(request, oid):
    account = Account.objects.filter(id=oid).first()
    if request.method == 'POST':
        form = CardForm(request.POST)
        if form.is_valid():
            card = form.save(commit=False)
            card.account_number = account
            card.save()
            messages.success(
                request, 'Card was successfully ordered!')
            return redirect('home')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = CardForm()
    context = {
        'account': account,
        'form': form
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
    cards = Card.objects.filter(account_number_id=oid)
    context = {
        'account': account,
        'cards': cards
    }
    return render(request, 'client/account.html', context)


@login_required
def card(request, oid, coid):
    account = Account.objects.filter(id=oid).first()
    card = Card.objects.filter(id=coid).first()
    context = {
        'account': account,
        'card': card
    }
    return render(request, 'client/card.html', context)
