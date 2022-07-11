from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from main.models import Renter, Organization
from django.views import View

class OrgLogin(View):
    return_url = None

    def get(self, request):
        OrgLogin.return_url = request.GET.get ('return_url')
        return render(request, 'main/org_login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        renter = Organization.get_org_by_email(email)
        error_message = None
        if renter:
            flag = True if password==renter.password else False
            print(flag)
            print(renter.password)
            if flag:
                request.session['org'] = renter.id

                if OrgLogin.return_url:
                    return HttpResponseRedirect(OrgLogin.return_url)
                else:
                    OrgLogin.return_url = None
                    return redirect('home')
            else:
                error_message = 'Неверный логин или пароль'
        else:
            error_message = 'Неверный логин или пароль'
        print(email, password)
        return render(request, 'main/org_login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')