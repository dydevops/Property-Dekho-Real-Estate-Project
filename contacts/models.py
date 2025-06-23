from django.db import models
from accounts.models import User
from realtors.models import Realtor
from listings.models import Listing,City
from datetime import datetime
from django.urls import reverse
from django.utils.text import slugify
# Create your models here.
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Contact(models.Model):
    page_name = models.CharField(max_length=100)
    meta_title      = models.CharField(max_length=150, blank=True)
    meta_description = models.TextField(max_length=300,blank=True)
    meta_keywords    = models.TextField(max_length=300,blank=True)
    bg_banner = models.ImageField(upload_to='photos/banner', blank=True)
    get_in_touch_title= models.CharField(max_length=300, default='Get in touch with us')
    description = models.TextField(max_length=500, blank=True)
    phone_no1 = models.CharField(max_length=100, blank=True)
    phone_no2 = models.CharField(max_length=100, blank=True)
    email1 = models.CharField(max_length=100, blank=True)
    email2 = models.CharField(max_length=100, blank=True)
    address1 = models.TextField(max_length=500, blank=True)
    address2 = models.TextField(max_length=500, blank=True)
    created_on = models.DateTimeField(blank=True, default=datetime.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    def __str__(self):
      return self.page_name
  

class ListingEnquiry(models.Model):
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE,blank=True,null=True)
    realtor  = models.ForeignKey(Realtor, on_delete=models.CASCADE,blank=True,null=True)
    listing_name = models.CharField(max_length=500,blank=True)
    listing_url = models.SlugField(max_length=700,blank=True)
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    phone_no = models.CharField(max_length=16, blank=True)
    city = models.CharField(max_length=100,null=True,blank=True)
    requirement = models.TextField(blank=True)
    user_id = models.IntegerField(blank=True)
    is_approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(blank=True, default=datetime.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        verbose_name_plural = 'Listing Enquiry'
    
    # @property
    # def full_name(self):
    #     return self.first_name
    
    def get_url(self):
        return reverse('listing', args=[self.city.slug, self.slug])
       
    def __str__(self):
        return self.full_name + ".... " + self.listing.title  
    
       
# Create your models here.
class Feedback(models.Model):
    full_name = models.CharField(max_length=100)
    subject = models.CharField(max_length=100,blank=True)
    email = models.EmailField(max_length=100)
    phone = models.CharField(max_length=18)
    message = models.TextField(blank=True)
    is_approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(blank=True, default=datetime.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        verbose_name = 'feedback'
        verbose_name_plural = 'feedback'
    def __str__(self):
        return self.email      