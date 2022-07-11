from django.shortcuts import render, redirect, HttpResponseRedirect
from django.contrib.auth.hashers import check_password
from main.models import Renter
from django.views import View

class Login(View):
    return_url = None

    def get(self, request):
        Login.return_url = request.GET.get ('return_url')
        return render(request, 'main/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        renter = Renter.get_customer_by_email(email)
        error_message = None
        if renter:
            flag = True if password==renter.password else False
            if flag:
                request.session['customer'] = renter.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)
                else:
                    Login.return_url = None
                    return redirect('home')
            else:
                error_message = 'Неверный логин или пароль'
        else:
            error_message = 'Неверный логин или пароль'
        print(email, password)
        return render(request, 'main/login.html', {'error': error_message})

def logout(request):
    request.session.clear()
    return redirect('login')