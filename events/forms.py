from django import forms
from .models import Event,Book
from django.contrib.auth.models import User


class UserSignup(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }


class UserLogin(forms.Form):
    username = forms.CharField(required=True)
    password = forms.CharField(required=True, widget=forms.PasswordInput())


class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        exclude=['organizer', 'seats_left']

        widgets={
        'date':forms.DateInput(attrs={'type':'date'}),
        'time':forms.TimeInput(attrs={'type':'time'}),
        }

class BookForm(forms.ModelForm):
    class Meta:
        model = Book
        exclude=['event','user','seats_left']

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields=['username', 'first_name', 'last_name', 'email' ,'password']

        widgets={
        'password': forms.PasswordInput(),
        }