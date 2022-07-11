from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect

from main.models import Organization, City, objectTypes, RentObject, ObjectPhotos, Comforts, RentNum, OrderList, Renter


def org_profile(request):
    id = request.session.get('org')
    profile = Organization.objects.get(id=id)
    cities = City.objects.all()
    obj_types = objectTypes.objects.all()
    comforts = Comforts.objects.all()
    obj_id = None
    booking = None
    rent_num = []
    try:
        obj_rent = RentObject.objects.filter(id_organization=id)
        for item in obj_rent:
            num = RentNum.objects.filter(id_rent_object=item.id)
            rent_num.append(num)
    except:
        obj_rent = None
    error_message = None
    if request.method == 'POST':
        if request.POST.get("form_type") == 'formOne':
            name = request.POST.get('name')
            phone = request.POST.get('phone')
            city = request.POST.get('city')
            address = request.POST.get('address')
            description = request.POST.get('descr')
            objType = request.POST.get('type')
            file = request.FILES.get('file')
            value = {
                'name': name,
                'phone': phone,
                'city': city,
                'address': address,
                'description': description,
                'objType': objType
            }
            obj = RentObject(name=name,
                             phone=phone,
                             city=city,
                             address=address,
                             description=description,
                             objectType=objType,
                             id_organization=id,
                             cover=file)
            error_message = validateRentObject(obj)
            error_message = None
            if not error_message:
                print(f"{name} {phone} {city} {address} {description} {objType}")
                obj.save()
                return redirect('org_profile')
        elif request.POST.get("form_type") == 'formTwo':
            kolvo = request.POST.get('kolvo')
            check1 = []
            check1.append( request.POST.get('check1'))
            check1.append( request.POST.get('check2'))
            check1.append( request.POST.get('check3'))
            check1.append( request.POST.get('check4'))
            check1.append( request.POST.get('check5'))
            check1.append( request.POST.get('check6'))
            check=""
            for item in check1:
                if item!=None:
                    check+=item+';'
            print(check)
            price = request.POST.get('price')
            files = request.FILES.getlist('file')
            obj_id = request.POST.get('obj_id')
            obj = RentNum(bed_count=kolvo,
                          is_free=True,
                          comfort=check,
                          price=price,
                          id_rent_object=obj_id)
            obj.save()
            for file in files:
                photo = ObjectPhotos(id_obj=obj.id, cover=file, id_rent_object=obj_id)
                photo.save()
            return redirect('org_profile')
        elif request.POST.get("form_type") == 'formThree':
            if '_edit' in request.POST:
                pass
            elif '_delete' in request.POST:
                obj_id = request.POST.get('obj_id')
                try:
                    record = RentNum.objects.get(id_rent_object=obj_id)
                    record.delete()
                except:
                    pass
                record = RentObject.objects.get(id=obj_id)
                record.delete()
                return redirect('org_profile')
            elif '_more' in request.POST:
                pass
            elif '_add' in request.POST:
                obj_id = request.POST.get('obj_id')
    booking = []
    for o in obj_rent:
        book = OrderList.objects.filter(id_rent_obj=o.id)
        booking.append(book)
    customer = Renter.objects.all()
    context = {
        'profile': profile,
        'cities': cities,
        'obj_types': obj_types,
        'error': error_message,
        'obj_rent': obj_rent,
        'comforts': comforts,
        'obj_id': obj_id,
        'rent_num': rent_num,
        'book': booking,
        'customer': customer,
    }
    return render(request, 'main/org_profile.html', context)

def validateRentObject(obj):
    error_message = None
    if (not obj.name):
        error_message = "Please Enter your First Name !!"
    elif len(obj.name) < 3:
        error_message = 'First Name must be 3 char long or more'
    elif not obj.phone:
        error_message = 'Enter your Phone Number'
    elif len(obj.phone) < 10:
        error_message = 'Phone Number must be 10 char Long'
    elif len(obj.description) < 10:
        error_message = 'Password must be 5 char long'
    return error_message