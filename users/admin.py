from django.contrib import admin
from .models import User

class UserAdmin(admin.ModelAdmin):
    list_display = ['email', 'first_name','last_name','is_verified' ,'auth_provider', 'created_at']


admin.site.register(User, UserAdmin)
