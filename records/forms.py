from django import forms
from .models import Record
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RecordForm(forms.ModelForm):
    class Meta:
        model = Record
        fields = '__all__'

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']
