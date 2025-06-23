from django.contrib import admin
from .models import Country,State,Developer,Project
# Register your models here.






admin.site.register(Country)
admin.site.register(State)
admin.site.register(Developer)
admin.site.register(Project)