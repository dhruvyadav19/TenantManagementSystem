from django.contrib import admin
from .models import Profile, Tenant
# Register your models here

class UserAdmin(admin.ModelAdmin):
    readonly_fields = ('id',)

admin.site.register(Profile, UserAdmin)
admin.site.register(Tenant)
