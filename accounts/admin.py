from django.contrib import admin
from .models import User,UserProfile,EnqEmailSetting,Author
from django.contrib.auth.admin import UserAdmin

# Register your models here.

class UserAdmin(UserAdmin):
    list_display = ('email', 'first_name', 'last_name', 'username', 'role', 'is_active')
    ordering = ('-date_joined',)
    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()



admin.site.register(User, UserAdmin)
admin.site.register(UserProfile)
admin.site.register(Author)
admin.site.register(EnqEmailSetting)