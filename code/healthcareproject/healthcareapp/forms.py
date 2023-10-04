from django.contrib.auth.forms import UserCreationForm
from .models import UserModel


class LoginForm(UserCreationForm):
    class Meta:
        model = UserModel
        fields = ('email', 'password')
