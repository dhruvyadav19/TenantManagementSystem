from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator, MinLengthValidator
# Create your models here.
class House(models.Model):
    house_number = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    landmark = models.CharField(max_length=200)
    apartment_choices = [
        ('AP', "Apartment"),
        ('SG', "Single Family House"),
        ('TW', "Town House"),
        ('CD', "Condominiums"),
        ('BG', "Bungalow"),
    ]
    property_type = models.CharField(max_length=200,
                                    choices = apartment_choices,
                                    default='AP')
    balcony = models.IntegerField()
    beds = models.IntegerField()
    pincode = models.CharField(max_length=6, validators=[MaxLengthValidator(limit_value=6), MinLengthValidator(limit_value=6)])
    rent = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    tenant_id = models.IntegerField(null=True, blank=True)
    occupied = models.BooleanField(default=False)
    E_Signature = models.CharField(max_length=100,null=True, blank=True)
    def __str__(self):
        return self.house_number

class Image(models.Model):
    house = models.ForeignKey(House,on_delete=models.CASCADE,related_name='house_pics')
    image = models.FileField(upload_to = "house_pics")

    def __str__(self):
        return self.house.house_number

class Amenities(models.Model):
    house = models.OneToOneField(House, on_delete=models.CASCADE)
    lift = models.BooleanField(default = False)
    air_conditioner = models.BooleanField(default = False)
    swimming_pool = models.BooleanField(default = False)
    gas_pipeline = models.BooleanField(default = False)
    visitor_parking = models.BooleanField(default = False)    
    gym = models.BooleanField(default = False)
    security = models.BooleanField(default = False)
    park = models.BooleanField(default = False)
    house_keeping = models.BooleanField(default = False)
    internet_services = models.BooleanField(default = False)
    shopping_center = models.BooleanField(default = False)
    power_backup = models.BooleanField(default = False)

    def __str__(self):
        return self.house.house_number
