import os

from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.shortcuts import render
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib.auth.models import User

# Create your views here.
from django.views.generic.base import View

from main import settings


class Home(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('staff_panel_login'))
        return render(request, 'tables/staff_panel_datatable.html')


class StaffLogin(View):
    def get(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('staff_panel_home'))
        return render(request, 'pages/staff_panel_login.html')

    def post(self, request):
        if request.user.is_authenticated():
            return HttpResponseRedirect(reverse('staff_panel_home'))

        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('staff_panel_home'))
        else:
            error = "Username password not match"
            return render(request, 'pages/staff_panel_login.html', {'error': error},status=401)


class StaffLogout(View):
    def get(self, request):
        logout(request)
        return HttpResponseRedirect(reverse('staff_panel_login'))


class EmailSubmissionForPasswordChange(View):
    def get(self, request):
        return render(request, 'pages/staff_panel_email_submission.html')

    def post(self, request):
        email_address = request.POST.get('email', "")
        mail = 0
        user = User.objects.filter(email=email_address)
        if len(user) > 0:
            password = user[0].password
            # forget password key user_id + qwertyqwerty + 10 char of hash password + username -> without special chars
            key = str(user[0].id) + "qwertyqwerty" + str(password)[:10] + "qwertyqwerty" + str(user[0].username)
            key = key[::-1]
            key = ''.join(e for e in key if e.isalnum())
            # print(key)
            subject = "Forgot password"
            message = "Hello " + user[0].username + "\n"
            message += "To continue forgot password please goto the link. \n"
            message += os.path.join(settings.STAFF_ADDR, 'forgot-password', key)
            # print(message)
            mail = send_mail(
                subject,
                message,
                settings.EMAIL_HOST_USER,
                [email_address],
                fail_silently=True,
            )

        return render(request, 'pages/staff_panel_email_submission.html', {'success': mail > 0})


class StaffForgotPassword(View):
    def get(self, request, code):
        code = code[::-1]
        invalid_code = True
        code_array = code.split('qwertyqwerty')
        try:
            user = User.objects.get(id=int(code_array[0]))
            password = str(user.password)[:10]
            password = ''.join(e for e in password if e.isalnum())
            if password == code_array[1]:
                invalid_code = False
                return render(request, 'pages/staff_panel_forgot_password.html',
                              {'invalid_code': invalid_code, 'user': user})
        except:
            print("error")
        return render(request, 'pages/staff_panel_forgot_password.html', {'invalid_code': invalid_code},status=400)

    def post(self, request, code):
        code = code[::-1]
        invalid_code = True
        code_array = code.split('qwertyqwerty')
        try:
            user = User.objects.get(id=int(code_array[0]))
            password = str(user.password)[:10]
            password = ''.join(e for e in password if e.isalnum())
            if password == code_array[1]:
                invalid_code = False
                new_password = request.POST.get("new-password")
                retype_password = request.POST.get("retype-password")
                if new_password == retype_password:
                    user.set_password(new_password)
                    user.save()
                    return HttpResponseRedirect(reverse('staff_panel_login'))
                else:
                    return render(request, 'pages/staff_panel_forgot_password.html',
                                  {"message": "Passwords don't match", 'invalid_code': invalid_code, 'user': user},status=400)
        except:
            print("error")
        return render(request, 'pages/staff_panel_forgot_password.html', {'invalid_code': invalid_code},status=400)


class StaffChangePassword(View):
    def get(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('staff_panel_login'))
        return render(request, 'forms/staff_panel_password_change.html')

    def post(self, request):
        if not request.user.is_authenticated():
            return HttpResponseRedirect(reverse('staff_panel_login'))
        old_password = request.POST.get("old-password", "")
        new_password = request.POST.get("new-password", "")
        retype_password = request.POST.get("retype-password", "")

        message = "Password change successful !"
        if request.user.check_password(old_password):
            if new_password == retype_password:
                request.user.set_password(new_password)
                request.user.save()
            else:
                message = "Please enter same password in both fields"
        else:
            message = "Enter your current valid password"
        return render(request, 'forms/staff_panel_password_change.html', {'message': message})
