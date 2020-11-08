from django import forms
from django.contrib.auth.models import User
from .models import House, Amenities, Contract

class HouseCreationForm(forms.ModelForm):
    class Meta:
        model = House
        fields = ['property_type','house_number','landmark','city','state','beds','pincode','rent','balcony']

class AmenitiesCreationForm(forms.ModelForm):
    class Meta:
        model = Amenities
        exclude = ['house']

class ContractForm(forms.ModelForm):
    class Meta:
        model = Contract
        fields = ['E_Signature']



