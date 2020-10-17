from django import forms
from django.contrib.auth.models import User
from .models import House

class HouseCreationForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['house_number','city','state','beds','pincode','rent']

