from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField

from accounts.models import User


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(label='password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'full_name', 'phone_number')

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValueError('password does not match')
        return cd['password2']

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password2'])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField(
        help_text="you can change the password <a href=\"../password/\">from this link</a>")

    class Meta:
        model = User
        fields = ('email', 'full_name', 'phone_number', 'password', 'last_login')


class UserRegisterForm(forms.Form):
    phone = forms.CharField(max_length=11)
    full_name = forms.CharField(max_length=100, label='full name')
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput)
