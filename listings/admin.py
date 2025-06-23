from django.contrib import admin
from .models import Listing,City,ListingGallery,FloorPlan,Amenities,ListingCategory,Configuration,Possession,Locality
# Register your models here.

class AmenitiesInline(admin.TabularInline):
    model = Amenities
    extra = 1
    
class GalleryInline(admin.TabularInline):
    model = ListingGallery
    extra = 1 
    
class FloorPlanInline(admin.TabularInline):
    model = FloorPlan
    extra = 1          

class ListingAdmin(admin.ModelAdmin):
  list_display = ('id', 'title','price','configuration','listing_type','city','realtor','status',)
  list_display_links = ('id', 'title')
  # prepopulated_fields = {'slug': ('title',)}
  list_filter = ('realtor','configuration')
  list_editable = ('status',)
  search_fields = ('title', 'description', 'address', 'city', 'state', 'zipcode', 'price')
  inlines = [AmenitiesInline,GalleryInline,FloorPlanInline]
  list_per_page = 25
  
class ListingCategoryAdmin(admin.ModelAdmin):
  list_display = ('id', 'category_name', 'status', 'created_on')
  list_display_links = ('id', 'category_name')
  prepopulated_fields = {'slug': ('category_name',)}
  list_per_page = 25 
  
class CityAdmin(admin.ModelAdmin):
  list_display = ('id', 'city_name', 'status', 'created_on')
  list_display_links = ('id', 'city_name')
  prepopulated_fields = {'slug': ('city_name',)}
  list_per_page = 25 
  
class LocalityAdmin(admin.ModelAdmin):
  list_display = ('id', 'local_name', 'status', 'created_on')
  list_display_links = ('id', 'local_name')
  prepopulated_fields = {'slug': ('local_name',)}
  list_per_page = 25      
  

admin.site.register(Listing, ListingAdmin)
admin.site.register(City,CityAdmin)
admin.site.register(ListingGallery)
admin.site.register(FloorPlan)
admin.site.register(Amenities)
admin.site.register(Configuration)
admin.site.register(Possession)
admin.site.register(Locality,LocalityAdmin)
admin.site.register(ListingCategory,ListingCategoryAdmin)
