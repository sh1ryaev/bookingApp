from datetime import datetime, timedelta
from django.shortcuts import render, redirect
from main.models import RentObject


def index(request):
    dt_start = datetime.now()
    dt_finish = dt_start + timedelta(days=1)
    rent_obj1 = RentObject.objects.filter(city='Казань')
    kolvo1 = len(rent_obj1)
    rent_obj2 = RentObject.objects.filter(city='Уфа')
    kolvo2 = len(rent_obj2)
    rent_obj3 = RentObject.objects.filter(city='Нижний Новгород')
    kolvo3 = len(rent_obj3)
    rent_obj4 = RentObject.objects.filter(city='Санкт-Петербург')
    kolvo4 = len(rent_obj4)
    context = {
        'start': dt_start.strftime('%Y-%m-%d'),
        'finish': dt_finish.strftime('%Y-%m-%d'),
        'kolvo1': kolvo1,
        'kolvo2': kolvo2,
        'kolvo3': kolvo3,
        'kolvo4': kolvo4,
    }
    return render(request, 'main/index.html', context)




