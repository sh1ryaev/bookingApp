import random

from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password
from main.models import Renter
from django.views import View
import smtplib




class Signup (View):
    def get(self, request):
        return render(request, 'main/reg.html')

    def post(self, request):
        is_send = False
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')
        code1 = postData.get('code')
        try:
            if len(code1)>0:
                is_send=True
        except:
            pass
        # validation
        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }
        error_message = None
        customer = Renter(first_name=first_name,
                             last_name=last_name,
                             phone=phone,
                             email=email,
                             password=password)
        error_message = self.validateCustomer(customer)

        if not error_message:
            print(first_name, last_name, phone, email, password)
            if is_send==False:
                # данные почтового сервиса
                usr = "shiryaev2001@gmail.com"
                passwd = "ay9PwgnYtD0cGm2Z"
                server = "smtp-relay.sendinblue.com"
                port = 587

                # тема письма
                subject = "Тестовое письмо от Python."
                # кому
                to = email
                # кодировка письма
                charset = 'Content-Type: text/plain; charset=utf-8'
                mime = 'MIME-Version: 1.0'
                # текст письма
                code = random.randint(1000, 9999)
                text = "Ваш код подтверждения " + str(code)
                # формируем тело письма
                body = "\r\n".join((f"From: {usr}", f"To: {to}",
                                f"Subject: {subject}", mime, charset, "", text))
                try:
                    # подключаемся к почтовому сервису
                    smtp = smtplib.SMTP(server, port)
                    smtp.starttls()
                    smtp.ehlo()
                    # логинимся на почтовом сервере
                    smtp.login(usr, passwd)
                    # пробуем послать письмо
                    smtp.sendmail(usr, to, body.encode('utf-8'))
                    is_send=True
                except smtplib.SMTPException as err:
                    print('Что - то пошло не так...')
                    raise err
                finally:
                    smtp.quit()
            try:
                if len(code1)>1:
                    customer.password = make_password(customer.password)
                    customer.register()
                    return redirect('home')
                else:
                    error_message='Код подтверждения неверен'
                    data = {
                    'error': error_message,
                    'values': value,
                    'is_send': is_send
                    }
                    return render(request, 'main/reg.html', data)
            except:
                error_message = 'Введите код подтверждения'
                data = {
                    'error': error_message,
                    'values': value,
                    'is_send': is_send
                }
                return render(request, 'main/reg.html', data)
        else:
            data = {
                'error': error_message,
                'values': value,
                'is_send': is_send
            }
            return render(request, 'main/reg.html', data)

    def validateCustomer(self, customer):
        error_message = None
        if (not customer.first_name):
            error_message = "Please Enter your First Name !!"
        elif len (customer.first_name) < 3:
            error_message = 'First Name must be 3 char long or more'
        elif not customer.last_name:
            error_message = 'Please Enter your Last Name'
        elif len (customer.last_name) < 3:
            error_message = 'Last Name must be 3 char long or more'
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