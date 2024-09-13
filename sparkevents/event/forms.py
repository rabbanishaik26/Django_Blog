from django import forms
from .models import Event,Registration
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['text', 'photo', 'location','capacity']

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['event']
        
class UserRegistrationForm(UserCreationForm):
    email = forms.EmailField() 
    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=150)
    password = forms.CharField(widget=forms.PasswordInput)
