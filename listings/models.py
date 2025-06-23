from django.db import models
from datetime import datetime
# from django.conf import settings
from django.utils.timezone import now
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django_ckeditor_5.fields import CKEditor5Field
from project.models import Country,State,Developer,Project
import uuid
from realtors.models import Realtor

# Create your models here.
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class City(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    city_name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=600,unique=True,blank=True, null=True)
    title = models.CharField(max_length=300,null=True,blank=True)
    photo= models.ImageField(upload_to='city/%Y/%m/%d/',null=True,blank=True)
    is_featured=models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        verbose_name = 'City'
        verbose_name_plural = '1. Cities'
        ordering = ['-created_on']
        
    def get_url(self):
            return reverse('property_by_city', args=[self.slug])     
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Runs the custom validation
        if not self.slug:
            self.slug = slugify(f"{self.city_name}-{self.pk}")
        super(City, self).save(*args, **kwargs) 
        
    def __str__(self):
        return self.city_name 
   
    
class Locality(models.Model):
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    local_name = models.CharField(max_length=300)
    slug = models.SlugField(max_length=600,unique=True,blank=True, null=True)
    title = models.CharField(max_length=300,null=True,blank=True)
    photo= models.ImageField(upload_to='locality/%Y/%m/%d/',null=True,blank=True)
    is_featured=models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        verbose_name = 'Locality'
        verbose_name_plural = '2. Localities'
        ordering = ['-created_on']
        
    def get_url(self):
            return reverse('property_by_locality', args=[self.slug])
             
    def save(self, *args, **kwargs):
        self.full_clean()  # Runs the custom validation
        if not self.slug:
            self.slug = slugify(f"{self.local_name}-{self.pk}")
        super(Locality, self).save(*args, **kwargs)  
        
    def __str__(self):
        return self.local_name    

class ListingCategory(models.Model):
    category_name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=350, unique=True,blank=True, null=True)
    meta_description = models.CharField(max_length=255,blank=True)
    meta_keywords = models.CharField(max_length=255, blank=True)
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='listingcategory/%Y/%m/%d/', blank=True)
    is_featured=models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        verbose_name = 'Listing Category'
        verbose_name_plural = '3. Listing categories'
        ordering = ['-created_on']
        
    # def get_url(self):
    #         return reverse('listing_by_category', args=[self.slug])     
    def save(self, *args, **kwargs):
        self.full_clean()  # Runs the custom validation
        # if not self.slug:
        self.slug = slugify(f"{self.category_name}-{self.pk}")
        super(ListingCategory, self).save(*args, **kwargs)      
        
    def __str__(self):
        return self.category_name
    
class Configuration(models.Model):
    name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=350, unique=True,blank=True,null=True)
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='configuration/%Y/%m/%d/', blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        verbose_name = 'Configuration'
        verbose_name_plural = '4. Configurations'
        ordering = ['-created_on']
        
    def save(self, *args, **kwargs):
        self.full_clean()  # Runs the custom validation
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.pk}")
        super(Configuration, self).save(*args, **kwargs)    
    
    def __str__(self):
        return self.name    

class Possession(models.Model):
    name = models.CharField(max_length=300, unique=True)
    slug = models.SlugField(max_length=350, unique=True,blank=True,null=True)
    description = models.TextField(max_length=500, blank=True)
    image = models.ImageField(upload_to='possession/%Y/%m/%d/', blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        verbose_name = 'Possession'
        verbose_name_plural = '5. Possessions'
        ordering = ['-created_on']
        
    def save(self, *args, **kwargs):
        self.full_clean()  # Runs the custom validation
        if not self.slug:
            self.slug = slugify(f"{self.name}-{self.pk}")
        super(Possession, self).save(*args, **kwargs)     
    
    def __str__(self):
        return self.name
    
    
class Listing(models.Model):
    listing_choices = (
        ('Buy', 'Buy'),
        ('Rent', 'Rent'),
    )
    sale_choices = (
        ('New Projects', 'New Projects'),
        ('Resale Properties', 'Resale Properties'),
    )
    title = models.CharField(max_length=400)
    slug            = models.SlugField(max_length=600, unique=True,null=True,blank=True)
    uuid = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    title_tag = models.CharField(max_length=255, default='Real Estate')
    meta_description = models.TextField(max_length=255, blank=True)
    meta_keywords = models.TextField(max_length=255, blank=True)
    country = models.ForeignKey(Country, on_delete=models.CASCADE, null=True,blank=True)
    state = models.ForeignKey(State, on_delete=models.CASCADE, null=True)
    city = models.ForeignKey(City, on_delete=models.CASCADE, null=True)
    locality = models.ForeignKey(Locality, on_delete=models.CASCADE,null=True,blank=True)
    location = models.CharField(max_length=600,null=True,blank=True)
    address = models.TextField(max_length=400,null=True)
    zipcode = models.CharField(max_length=20,null=True,blank=True)
    description = CKEditor5Field(config_name='extends',blank=True, null=True)
    mrp_price   = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, default=0,blank=True)
    bedrooms = models.IntegerField()
    bathrooms = models.DecimalField(max_digits=2, decimal_places=1)
    parking = models.IntegerField(blank=True, null=True)
    sqft = models.IntegerField()
    lot_size = models.CharField(max_length=200,null=True,blank=True)
    floors = models.CharField(max_length=300,null=True,blank=True)
    category = models.ForeignKey(ListingCategory, on_delete=models.CASCADE,null=True,blank=True)
    configuration = models.ForeignKey(Configuration, on_delete=models.CASCADE,null=True,blank=True)
    possession = models.ForeignKey(Possession, on_delete=models.CASCADE,null=True,blank=True)
    listing_type=models.CharField(choices=listing_choices, max_length=150,null=True,blank=True)
    sale_type=models.CharField(choices=sale_choices, max_length=150,null=True,blank=True)
    photo_main = models.ImageField(upload_to='photos/%Y/%m/%d/')
    youtube_video_code = models.CharField(max_length=400,null=True,blank=True)
    floor_plan_pdf= models.FileField(upload_to='floorplan/pdf/%Y/%m/%d/',null=True,blank=True)
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE,null=True,blank=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE,null=True,blank=True)
    realtor = models.ForeignKey(Realtor, on_delete=models.CASCADE,null=True,blank=True)
    is_featured=models.BooleanField(default=False)
    is_published = models.BooleanField(default=True)
    list_date = models.DateTimeField(default=datetime.now, blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        verbose_name = 'Listing'
        verbose_name_plural = '6. Listings'
        ordering = ['-created_on']
    
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Runs the custom validation
        if not self.slug:
            self.slug = slugify(f"{self.configuration.name}-flat-{self.title}-{self.locality.local_name}-{str(self.uuid)[:8]}")
        super(Listing, self).save(*args, **kwargs)
        
    # def save(self, *args, **kwargs):
    #     if not self.slug_en and self.recipe_name:
    #         self.slug_en = slugify(self.recipe_name)
    #     super().save(*args, **kwargs)
    #     if not self.code:
    #         self.code = f"{self.pk}"
    #         super().save(update_fields=["code"])
    #     else:
    #         super().save(*args, **kwargs)    
    
    # def get_url(self):
    #        return reverse('listing', args=[self.slug])
    def get_url(self):
        return reverse('listing', args=[self.city.slug, self.slug])
         
    def __str__(self):
      return self.title
  
class ListingGallery(models.Model):
    listing = models.ForeignKey(Listing, default=None, on_delete=models.CASCADE,null=True,blank=True)
    image = models.ImageField(upload_to='listing/gallery', max_length=255)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)

    def __str__(self):
        return self.listing.title

    class Meta:
        verbose_name = 'Gallery'
        verbose_name_plural = '7. Gallery'
        ordering = ['-created_on'] 

class FloorPlan(models.Model):
    listing = models.ForeignKey(Listing, default=None, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=100)
    photo= models.ImageField(upload_to='floorplan/photo/%Y/%m/%d/',null=True,blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        verbose_name = 'Floor Plan'
        verbose_name_plural = '8. Floor Plans'
        ordering = ['-created_on']
  
    def __str__(self):
        return self.name + ".... " + self.listing.title   
                
class Amenities(models.Model):
    listing = models.ForeignKey(Listing, default=None, on_delete=models.CASCADE,null=True,blank=True)
    name = models.CharField(max_length=300)
    photo= models.ImageField(upload_to='amenities/photo/%Y/%m/%d/',null=True,blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        verbose_name = 'Amenities'
        verbose_name_plural = '9. Amenities'
        ordering = ['-created_on']
  
    # def __str__(self):
    #     return self.name
    def __str__(self):
        return self.name + ".... " + self.listing.title
                      