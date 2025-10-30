from django import forms
from django.contrib.auth.models import User

class UserForm(forms.ModelForm):
    password_confirmation = forms.CharField()
    
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'password', ]
        