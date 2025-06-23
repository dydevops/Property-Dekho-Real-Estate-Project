from django.contrib import admin
from .models import Realtor,EmailSetting
# Register your models here.

class RealtorAdmin(admin.ModelAdmin):
  list_display = ('id', 'name', 'email','slug','hire_date')
  list_display_links = ('id', 'name')
  prepopulated_fields = {'slug': ('name',)}
  search_fields = ('name',)
  list_per_page = 25

admin.site.register(Realtor, RealtorAdmin)
admin.site.register(EmailSetting)