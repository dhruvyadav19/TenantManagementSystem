from django import forms
from django.forms import ModelForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from houses.models import House, Amenities
from users.models import Profile
from .models import Payment, Complaint
from django.core.validators import MaxLengthValidator, MinLengthValidator

class PayRentForm(forms.Form):
    name = forms.CharField(max_length=100)
    card_number = forms.CharField(max_length=12, validators=[MinLengthValidator(12)])
    expiry_date = forms.CharField(max_length=5, validators=[MinLengthValidator(5)])
    cvv = forms.CharField(max_length=3, validators=[MinLengthValidator(3)])
    rent = forms.IntegerField()

class ComplaintsForm(ModelForm):
    class Meta:
        model = Complaint
        fields = ['complaint_type', 'complaint']
