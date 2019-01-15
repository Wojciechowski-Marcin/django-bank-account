from client.models import *

city1 = City(postal_code='50-370', city='Wrocław')
city1.save()
address1 = Address(id=0, street="wybrzeże Stanisława Wyspiańskiego",
                   house_nr=27, city=city1)
address1.save()
su = CustomUser.objects.create_superuser(password='testing321', username='Wojciechowski-Marcin', first_name='Marcin', last_name='Wojciechowski',

                                         email='wojc.marcin@gmail.com', pesel=1234567891, telephone=123456789, address=address1, birth_day='2000-11-11 11:11')
su.save()
account = Account(account_number='11111111111111111111111', user=su,
                  balance=100.40, transaction_limit='10', is_active=True, account_type='1', currency='PLN')
account.save()

account2 = Account(account_number='12345678912345678912345', user=su,
                   balance=0.40, transaction_limit='10', is_active=True, account_type='2', currency='JPY')
account2.save()

card = Card(account_number=account, card_number='1234567890123456',
            cvv='123', is_nfc='0', is_active='1', transaction_limit='123')
card.save()

transaction = TransactionHistory(
    source_bank_account=account, destination_bank_account=account2, title='tytul', amount=10.40)
transaction.save()
