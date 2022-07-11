from django.shortcuts import render

from main.models import Favourite, RentObject


def favourite(request):
    id_renter = request.session.get('customer')
    favourite = Favourite.objects.filter(id_renter=id_renter)
    r_obj = []
    for f in favourite:
        rent_obj = RentObject.objects.filter(id=f.id_rent_obj)
        rj = rent_obj.first()
        if rj not in r_obj:
            r_obj.append(rj)
    context = {
        'rent_obj': r_obj,
    }
    return render(request, 'main/favoutite.html', context)