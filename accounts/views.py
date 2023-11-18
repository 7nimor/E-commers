import random

from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegisterForm, UserRegisterVerifyForm, UserLoginForm
from utils import send_otp_code
from .models import OtpCode, User


class UserRegisterView(View):
    form_class = UserRegisterForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/register.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000, 9999)
            send_otp_code(form.cleaned_data['phone'], random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'], code=random_code)
            request.session['user_registration_info'] = {
                'phone': form.cleaned_data['phone'],
                'email': form.cleaned_data['email'],
                'full_name': form.cleaned_data['full_name'],
                'password': form.cleaned_data['password']
            }
            messages.success(request, 'we sent your OTP code', 'success')
            return redirect('accounts:user_verify')
        return render(request, 'accounts/register.html', {'form': form})


class UserVerifyCodeView(View):
    form_class = UserRegisterVerifyForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/verify.html', {'form': form})

    def post(self, request):
        info = request.session['user_registration_info']
        otp_code = OtpCode.objects.get(phone_number=info['phone'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            if cd['code'] == str(otp_code.code):
                User.objects.create_user(
                    email=info['email'],
                    full_name=info['full_name'],
                    phone_number=info['phone'],
                    password=info['password']
                )
                otp_code.delete()
                messages.success(request, 'you registered.', 'success')
                return redirect('home:home')
            else:
                messages.error(request, 'your code is wrong', 'danger')
                return redirect('accounts:user_verify')
        return redirect('home:home')


class UserLogOutView(LoginRequiredMixin, View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged', 'success')
        return redirect('home:home')


class UserLoginView(View):
    form_class = UserLoginForm

    def get(self, request):
        form = self.form_class
        return render(request, 'accounts/login.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, phone_number=cd['phone'], password=cd['password'])
            if user:
                login(request, user)
                messages.success(request, 'you are logged in', 'success')
                return redirect('home:home')
            messages.error(request, 'your phone or password is wrong', 'danger')
        return render(request, 'accounts/login.html', {'form': form})
