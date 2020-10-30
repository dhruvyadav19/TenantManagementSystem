from django.contrib import admin
from .models import House,Image,Amenities
# Register your models here.

class HouseAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(House, HouseAdmin)
admin.site.register(Image)
admin.site.register(Amenities)