from django.shortcuts import render

from main.models import Renter, OrderList, RentNum


def profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        phone = request.POST.get('phone')
        id = request.session.get('customer')
        profile = Renter.objects.get(id=id)
        profile.first_name = first_name
        profile.last_name = last_name
        profile.phone = phone
        profile.save()
    id = request.session.get('customer')
    profile = Renter.objects.get(id=id)
    book = OrderList.objects.filter(id_renter=id)
    context = {
        'profile': profile,
        'book': book,
    }
    return render(request, 'main/account.html', context)
