from django.db import models
from django.contrib.auth.models import User
# Create your models here.
class House(models.Model):
    house_number = models.CharField(max_length=200)
    city = models.CharField(max_length=200)
    state = models.CharField(max_length=200)
    beds = models.IntegerField()
    pincode = models.IntegerField()
    rent = models.IntegerField()
    user = models.ForeignKey(User,on_delete=models.CASCADE)

    def __str__(self):
        return self.house_number

class Image(models.Model):
    house = models.ForeignKey(House,on_delete=models.CASCADE,related_name='house_pics')
    image = models.FileField(upload_to = "house_pics")

    def __str__(self):
        return self.house.house_number