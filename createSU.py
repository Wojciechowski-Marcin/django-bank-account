from client.models import CustomUser, Address, City

city1 = City(postal_code='50-370', city='Wrocław')
city1.save()
address1 = Address(id=0, street="wybrzeże Stanisława Wyspiańskiego",
                   house_nr=27, city=city1)
address1.save()
su = CustomUser.objects.create_superuser(password='testing321', username='Wojciechowski-Marcin', first_name='Marcin', last_name='Wojciechowski',
                                         email='wojc.marcin@gmail.com', pesel=1234567891, telephone=123456789, address=address1, birth_day='2000-11-11 11:11')
su.save()
