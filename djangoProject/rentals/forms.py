from django import forms
from django.contrib.auth.models import User
from houses.models import House, Amenities
from .models import Payment

class PayRentForm(forms.Form):
    name = forms.CharField(max_length=100)
    card_number = forms.CharField(max_length=12)
    expiry_date = forms.CharField(max_length=5)
    cvv = forms.CharField(max_length=3)
    rent = forms.IntegerField()
