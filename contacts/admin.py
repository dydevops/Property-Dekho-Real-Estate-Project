from django.contrib import admin
from .models import Contact,ListingEnquiry,Feedback
# Register your models here.

# class ContactAdmin(admin.ModelAdmin):
#   list_display = ('id', 'name', 'email',)
#   list_display_links = ('id', 'name')
#   search_fields = ('name', 'email',)
#   list_per_page = 25

admin.site.register(Contact)
admin.site.register(ListingEnquiry)
admin.site.register(Feedback)