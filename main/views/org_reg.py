from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from main.models import Organization
from django.views import View


class OrgSignup (View):
    def get(self, request):
        return render(request, 'main/org_reg.html')

    def post(self, request):
        postData = request.POST
        name = postData.get('name')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        # validation
        value = {
            'name': name,
            'phone': phone,
            'email': email
        }
        error_message = None

        customer = Organization(name=name,
                             phone=phone,
                             email=email,
                             password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            print(name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('home')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'main/org_reg.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.name):
            error_message = "Please Enter your First Name !!"
        elif len (customer.name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.phone:
            error_message = 'Enter your Phone Number'
        elif len (customer.phone) < 10:
            error_message = 'Phone Number must be 10 char Long'
        elif len (customer.password) < 5:
            error_message = 'Password must be 5 char long'
        elif len (customer.email) < 5:
            error_message = 'Email must be 5 char long'
        elif customer.isExists ():
            error_message = 'Email Address Already Registered..'
        # saving

        return error_message