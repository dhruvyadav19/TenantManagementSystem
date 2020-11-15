from django.contrib import admin
from .models import Profile
# Register your models here

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Profile, UserAdmin)
