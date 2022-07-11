from datetime import time, datetime, timedelta
from functools import partial

from django.db.models import Q
from geopy.geocoders import Nominatim
from django.http import HttpResponse
from django.shortcuts import render

from main.models import RentNum, ObjectPhotos, RentObject, Renter, OrderList
from main.views.catalog import Comfort


def rentobject(request):
    id = request.GET.get("obj_id", 1)
    start = request.GET.get("start")
    finish = request.GET.get("finish")
    book_id = request.GET.get('book_id')
    doorder = request.GET.get('doorder')

    booking_num = None
    message = None
    isPrice = 'No'
    summa = 0
    try:
        dt_start = datetime.strptime(start, '%Y-%m-%d')
        dt_finish = datetime.strptime(finish, '%Y-%m-%d')
    except:
        dt_start = datetime.now()
        dt_finish = dt_start + timedelta(days=1)
    kolvo = request.GET.get("kolvo", 1)
    dt = dt_finish - dt_start
    cnt_days = dt.days
    if request.method == 'POST':
        start = request.POST.get('start')
        finish = request.POST.get('finish')
        obj_id = request.POST.get('obj_id')
        try:
            dt_start = datetime.strptime(start, '%Y-%m-%d')
            dt_finish = datetime.strptime(finish, '%Y-%m-%d')
        except:
            dt_start = datetime.now()
            dt_finish = dt_start + timedelta(days=1)
        dt = dt_finish - dt_start
        cnt_days = dt.days
        id = request.POST.get("id", 1)
        isPrice = request.POST.get('isPrice')

    if isPrice == 'yes':
        rent_num = RentNum.objects.filter(id_rent_object=obj_id)
        book = OrderList.objects.all()
        ids = []
        for b in book:
            if b.start_date < dt_start.date() and b.finish_date > dt_finish.date():
                ids.append(b.id_rent_num)
        for i in ids:
            print(i)
        rnt = []
        for r in rent_num:
            if r.id not in ids:
                rnt.append(r)
        if book_id:
            pass
        else:
            booking_num = RentNum.objects.filter(id=id)
            booking_num = booking_num.first()
            summa = booking_num.price * cnt_days

        photos = ObjectPhotos.objects.filter(id_rent_object=obj_id)
        mainphoto = photos.first()
        rn = rent_num.first()
        rent_obj = RentObject.objects.filter(id=rn.id_rent_object)
        rent_obj = rent_obj.first()
    else:
        rent_num = RentNum.objects.filter(id_rent_object=id)
        book = OrderList.objects.all()
        ids = []
        for b in book:
            if b.start_date<dt_start.date() and b.finish_date>dt_finish.date():
               ids.append(b.id_rent_num)
        for i in ids:
            print(i)
        rnt = []
        for r in rent_num:
            if r.id not in ids:
                rnt.append(r)
        if book_id:
            pass
        else:
            book_id = request.POST.get('book_id')
            try:
                booking_num = RentNum.objects.filter(id=book_id)
                booking_num = booking_num.first()
            except:
                pass
            try:
                summa = booking_num.price * cnt_days
            except:
                summa = 0
        photos = ObjectPhotos.objects.filter(id_rent_object=id)
        mainphoto = photos.first()
        rent_obj = RentObject.objects.filter(id=id)
        rent_obj = rent_obj.first()


    com = ''
    try:
        id = request.session.get('customer')
        profile = Renter.objects.get(id=id)
    except:
        profile = None
    comforts = []
    for pn in rent_num:
        comfort = Comfort(key=pn.id_rent_object, comfort=pn.comfort.split(';'))
        com=comfort=pn.comfort.split(';')
        com.remove('')
        comforts.append(comfort)
    geolocator = Nominatim(user_agent="nominatim")
    location = geolocator.geocode(rent_obj.address+" "+rent_obj.city)
    if location == None:
        longitude = 0;
        latitude = 0;
    else:
        longitude = location.longitude
        latitude = location.latitude
    if doorder:
        start = request.GET.get("start")
        print(start)
        finish = request.GET.get("finish")
        print(finish)

        dt_start = datetime.strptime(start, '%Y-%m-%d')
        dt_finish = datetime.strptime(finish, '%Y-%m-%d')
        summa = request.GET.get('summa')
        order = OrderList(id_renter=profile.id,id_rent_obj=rent_obj.id ,id_rent_num=book_id,start_date=dt_start.strftime('%Y-%m-%d'),
                          finish_date=dt_finish.strftime('%Y-%m-%d'),summ=summa)
        order.save()
        message = 'Бронирование прошло успешно!'
    context={
        'rent_num': rnt,
        'photos': photos,
        'mainphoto': mainphoto,
        'rent_obj': rent_obj,
        'profile': profile,
        'comforts': comforts,
        'comfort': com,
        'cnt_days': cnt_days,
        'summa': summa,
        'start': dt_start.strftime('%Y-%m-%d'),
        'finish': dt_finish.strftime('%Y-%m-%d'),
        'booking_num': booking_num,
        'message': message,
        'longitude': longitude,
        'latitude': latitude,
    }
    return render(request, 'main/rent-object.html', context)