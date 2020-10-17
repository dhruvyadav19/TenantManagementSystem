from django.db import models
from django.contrib.auth.models import User
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
