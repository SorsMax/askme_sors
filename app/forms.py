from django import forms
from django.views.decorators.csrf import csrf_exempt

class LoginForm(forms.Form):
    login = forms.CharField(max_length=40)
    password = forms.CharField(max_length=20)
