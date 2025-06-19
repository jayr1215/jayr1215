from django import forms
from django import forms
from .models import Appointment, Patient
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User

class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))


class AppointmentForm(forms.ModelForm):
    PURPOSE_CHOICES = [
        ('Prophylaxis', 'Prophylaxis'),
        ('Dental Fillings', 'Dental Fillings'),
        ('Removable Dentures', 'Removable Dentures'),
        ('Tooth Extractions', 'Tooth Extractions'),
        ('Dental Checkups & Diagnosis', 'Dental Checkups & Diagnosis'),
        ('Crowns & Bridges', 'Crowns & Bridges'),
        ('Orthodontics', 'Orthodontics'),
    ]

    name = forms.CharField(max_length=100, required=True)
    age = forms.IntegerField(min_value=0, required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    email = forms.EmailField(required=True)
    purpose_of_appointment = forms.ChoiceField(choices=PURPOSE_CHOICES, required=True)
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}), required=True)
    time = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}), required=True)

    class Meta:
        model = Appointment
        fields = [
            'name', 'age', 'phone_number', 'email',
            'purpose_of_appointment', 'date', 'time'
        ]


class UserRegisterForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True)
    last_name = forms.CharField(max_length=100, required=True)
    email = forms.EmailField(required=True) # Add this line

    ROLE_CHOICES = [
        ('patient', 'Patient'),
        ('admin', 'Admin'),
    ]
    role = forms.ChoiceField(choices=ROLE_CHOICES, required=True, initial='patient')

    class Meta(UserCreationForm.Meta):
        model = User
        fields = UserCreationForm.Meta.fields + ('first_name', 'last_name', 'email', 'role',) # Add 'email' and 'role' to fields

    def save(self, commit=True):
        user = super().save(commit=False)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.email = self.cleaned_data['email'] # Save email to user object
        if commit:
            user.save()
        return user

class PatientProfileForm(forms.ModelForm):
    class Meta:
        model = Patient
        fields = ['first_name', 'last_name', 'phone_number', 'email', 'date_of_birth', 'address']
        widgets = {
            'date_of_birth': forms.DateInput(attrs={'type': 'date'}),
        }
