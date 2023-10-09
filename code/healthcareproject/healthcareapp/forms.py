from django.contrib.auth.forms import UserCreationForm
from .models import UserModel
from django import forms



class LoginForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'password')

class uploadFormExcel(forms.Form):
    file = forms.FileField()