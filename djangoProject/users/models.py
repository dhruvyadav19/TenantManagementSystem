from django.db import models
from django.contrib.auth.models import User
from houses.models import House
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    firstName = models.CharField(max_length=20,blank=True)
    lastName = models.CharField(max_length=20,blank=True)
    image = models.ImageField(default='default.jpg',upload_to='profile_pics')
    contact = models.CharField(max_length=10,blank=True)
    def __str__(self):
        return f'{self.user.username} Profile'

class Tenant(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    house = models.OneToOneField(House, on_delete=models.CASCADE, default=19)
    due_date = models.DateField(auto_now_add=True)
    apartment_choices = [
        ('PL', "Plumbing"),
        ('EL', "Electrical"),
        ('Rv', "Renovation"),
        ('Ot', "Others"),
    ]
    complaint_type = models.CharField(max_length=200,
                                    choices = apartment_choices,
                                    default='Ot')
    complaint = models.CharField(max_length=200, blank=True)

    def __str__(self):
        return self.user.id
