from django.db import models
from django.contrib.auth.models import User
from houses.models import House
# Create your models here.

class Payment(models.Model):
    house = models.OneToOneField(House,on_delete=models.CASCADE)
    start_date = models.DateTimeField()
    is_rent_due = models.BooleanField(default=True)
    total_amount_paid = models.IntegerField(default=0)
    due_money = models.IntegerField()
    tenant_id = models.IntegerField()
    last_payment_date = models.DateTimeField(null=True)

    def __str__(self):
        return self.house.house_number