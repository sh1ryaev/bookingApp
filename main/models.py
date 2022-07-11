from django.db import models


class Task(models.Model):
    title = models.CharField('Название', max_length=50)
    task = models.TextField('Описание')

    def __str__(self):
        return self.title
    class Meta:
        verbose_name='Задача'
        verbose_name_plural='Задачи'


class Organization(models.Model):
    name = models.CharField('Наименование организации', max_length=50)
    email = models.CharField('Email', max_length=50)
    password = models.CharField('Пароль', max_length=50)
    phone = models.CharField('Телефон', max_length=11)

    def __str__(self):
        return self.name

    # to save the data
    def register(self):
        self.save()

    @staticmethod
    def get_org_by_email(email):
        try:
            return Organization.objects.get(email=email)
        except:
            return False

    def isExists(self):
        if Organization.objects.filter(email=self.email):
            return True
        return False


class City(models.Model):
    name = models.CharField('Наименование города', max_length=200)


class objectTypes(models.Model):
    name = models.CharField('Наименование типа объекта', max_length=50)



class ObjectPhotos(models.Model):
    id_obj = models.BigIntegerField('Номер объекта')
    cover = models.ImageField(upload_to='images/%Y-%m-%d/')
    id_rent_object = models.BigIntegerField('Номер объекта', default=1)


class RentObject(models.Model):
    name = models.CharField('Имя', max_length=100, default='name')
    phone = models.CharField('Телефон', max_length=11)
    city = models.CharField('Город', max_length=30)
    address = models.CharField('Адрес', max_length=100)
    id_organization = models.BigIntegerField('Номер организации')
    description = models.TextField('Описание объекта')
    objectType = models.CharField('Тип объекта', max_length=50)
    cover = models.ImageField(upload_to='images/%Y-%m-%d/', default='/images/default.png')



class Comforts(models.Model):
    name = models.CharField('Удобства', max_length=100)

class RentNum(models.Model):
    bed_count = models.IntegerField('Количество спальных мест')
    is_free = models.BooleanField('Свободен ли')
    comfort = models.CharField(max_length=100)
    price = models.IntegerField('Цена за сутки')
    id_rent_object = models.BigIntegerField('Номер объекта')


class Renter(models.Model):
    first_name = models.CharField('Имя', max_length=50)
    last_name = models.CharField('Фамилия', max_length=50)
    password = models.CharField('Пароль', max_length=50)
    phone = models.CharField('Телефон', max_length=11)
    email = models.CharField('Email', max_length=50)
    card_num = models.CharField('Номер карты', max_length=16)

    # to save the data
    def register(self):
        self.save()

    @staticmethod
    def get_customer_by_email(email):
        try:
            return Renter.objects.get(email=email)
        except:
            return False

    def isExists(self):
        if Renter.objects.filter(email=self.email):
            return True
        return False


class Order(models.Model):
    summ = models.IntegerField('Сумма заказа')


class OrderList(models.Model):
    id_renter = models.IntegerField('Номер арендатора')
    id_rent_num = models.IntegerField('Номер номера')
    id_rent_obj = models.IntegerField('Номер объекта', default=1)
    start_date = models.DateField('Дата заезда')
    finish_date = models.DateField('Дата выезда')
    summ = models.IntegerField('Сумма заказа', default=0)


class Favourite(models.Model):
    id_renter = models.IntegerField('Номер арендатора')
    id_rent_obj = models.IntegerField('Номер объекта', default=1)


