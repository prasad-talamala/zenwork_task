from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class RegistrationForm(UserCreationForm):
    first_name = forms.CharField(max_length=100, required=True,
                                 widget=forms.TextInput(attrs={'class': 'form-control'}),
                                 help_text="Required. please enter your first name.")
    last_name = forms.CharField(max_length=100, required=True,
                                widget=forms.TextInput(attrs={'class': 'form-control'}),
                                help_text="Required. please enter your last name.")
    email = forms.EmailField(max_length=100, required=True,
                             widget=forms.EmailInput(attrs={'class': 'form-control'}),
                             help_text="Required. please enter your personal email id.")

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']
