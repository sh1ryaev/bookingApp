from datetime import datetime, timedelta
from django.shortcuts import render
from django.db.models import Q
from main.models import RentObject, ObjectPhotos, objectTypes, RentNum, Favourite


def catalog(request):
    rent_obj = RentObject.objects.all()
    photo = ObjectPhotos.objects.all()
    obj_types = objectTypes.objects.all()
    add_fav = request.GET.get('add_fav')
    del_fav = request.GET.get('del_fav')
    kolvo = 1
    filter = Filter('', '', '', '1', '')
    key = None
    if request.method == 'GET':
        place = request.GET.get("city", 'Казань')
        type_get = request.GET.get("ctg",'')
        if type_get!='':
            rent_obj = RentObject.objects.filter(objectType=type_get, city=place)
        else:
            rent_obj = RentObject.objects.filter(city=place)
        key = []
        comforts = []
        price_num = RentNum.objects.all()
        for pn in price_num:
            if pn.id_rent_object not in key and pn.bed_count>=int(kolvo):
                key.append(pn.id_rent_object)
                comfort = Comfort(key=pn.id_rent_object, comfort=pn.comfort.split(';'))
                comforts.append(comfort)
        filter = Filter(place, '', '', '1', '')
    ctg = []
    for item in obj_types:
        ctg.append(item.name)
    filter.obj_types=ctg
    if request.method == 'POST':
        place = request.POST.get('place')
        start = request.POST.get('start')
        finish = request.POST.get('finish')

        kolvo = request.POST.get('kolvo')
        min = request.POST.get('min')
        max = request.POST.get('max')
        check1 = request.POST.get('check1')
        if check1==None:
            check1=''
        check2 = request.POST.get('check2')
        if check2==None:
            check2=''
        check3 = request.POST.get('check3')
        if check3==None:
            check3=''
        check4 = request.POST.get('check4')
        if check4==None:
            check4=''
        if check1=='' and check2=='' and check3=='' and check4=='':
            check1='Отель'
            check2='Хостел'
            check3='Аппартаменты'
            check4='Коттедж'

        try:
            rent_obj = RentObject.objects.filter(Q(city=place), Q(objectType=check1) | Q(objectType=check2)
                                          | Q(objectType=check3) | Q(objectType=check4))
        except:
            rent_obj = RentObject.objects.filter(city=place)
        try:
            price_num = RentNum.objects.filter(price__lte=max, price__gte=min)
        except:
            price_num = RentNum.objects.all()
        key = []
        comforts = []
        prc_num = []
        for pn in price_num:
            if pn.id_rent_object not in key and pn.bed_count>=int(kolvo):
                key.append(pn.id_rent_object)
                comfort = Comfort(key=pn.id_rent_object, comfort=pn.comfort.split(';'))
                comforts.append(comfort)
        filter = Filter(place,start,finish,kolvo,ctg)
    try:
        dt_start = datetime.strptime(start, '%Y-%m-%d')
        dt_finish = datetime.strptime(finish, '%Y-%m-%d')
    except:
        dt_start = datetime.now()
        dt_finish = dt_start + timedelta(days=1)
    print(kolvo)
    if add_fav:
        try:
            id_renter = request.session.get('customer')
            fav = Favourite(id_renter=id_renter, id_rent_obj=add_fav)
            fav.save()
        except:
            pass
    if del_fav:
        try:
            id_renter = request.session.get('customer')
            fav = Favourite.objects.get(id_renter=id_renter, id_rent_obj=del_fav)
            fav.delete()
        except:
            pass
    fvrt = []
    try:
        id_renter = request.session.get('customer')
        favor = Favourite.objects.filter(id_renter=id_renter)
        for fv in favor:
            print(fv.id_rent_obj)
            if fv.id_rent_obj in key:
                fvrt.append(fv.id_rent_obj)
                print(fv)
    except:
        pass


    context = {
        'rent_obj': rent_obj,
        'photo': photo,
        'filter': filter,
        'price_num': price_num,
        'key': key,
        'comforts': comforts,
        'start': dt_start.strftime('%Y-%m-%d'),
        'finish': dt_finish.strftime('%Y-%m-%d'),
        'fvrt': fvrt,

    }
    return render(request, 'main/catalog.html', context)

class Filter():
    def __init__(self, place, start, finish, kolvo, obj_types):
        self.place=place
        self.start=start
        self.finish=finish
        self.kolvo=kolvo
        self.obj_types=obj_types

class Comfort():
    def __init__(self, key, comfort):
        self.key=key
        self.comfort = comfort
