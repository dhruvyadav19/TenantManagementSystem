from django.contrib import admin
from .models import House,Image,Amenities, Contract
# Register your models here.

class HouseAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(House, HouseAdmin)
admin.site.register(Image)
admin.site.register(Amenities)
admin.site.register(Contract)