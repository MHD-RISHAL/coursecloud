from django import forms
from instructor.models import User
from django.contrib.auth.forms import UserCreationForm


class StudentReg(UserCreationForm):
    class Meta:
        model=User
        fields = ["email", "username", "password1", "password2"]



class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


