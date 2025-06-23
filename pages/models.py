from django.db import models
from django.utils.timezone import now
from django.utils import timezone
from datetime import datetime
from django.urls import reverse
from django.db.models.fields.related import ForeignKey, OneToOneField
from django_ckeditor_5.fields import CKEditor5Field
from ckeditor_uploader.fields import RichTextUploadingField
# Create your models here.
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class General(models.Model):
    website_name = models.CharField(max_length=100, default='Property Dekhoge')
    meta_title = models.CharField(max_length=100, default='Property Dekhoge')
    meta_description = models.TextField(max_length=300,blank=True)
    meta_keywords = models.TextField(max_length=300,blank=True)
    google_meta_tag = models.CharField(max_length=500, blank=True)
    website_url = models.URLField(max_length=200, blank=True)
    favicon = models.ImageField(upload_to='favicon', blank=True)
    logo= models.ImageField(upload_to='logo', blank=True)
    footer_logo= models.ImageField(upload_to='logo', blank=True)
    content = models.TextField(max_length=300,blank=True,null=True)
    phone_no1 = models.CharField(max_length=50,blank=True)
    phone_no2 = models.CharField(max_length=50,blank=True)
    email1 = models.EmailField(max_length=200,blank=True)
    email2 = models.EmailField(max_length=200,blank=True)
    whatsapp_link = models.URLField(max_length=300, blank=True)
    address = models.TextField(max_length=300,blank=True)
    facebook_link = models.URLField(max_length=200, blank=True)
    linkedin_link = models.URLField(max_length=200, blank=True)
    instagram_link = models.URLField(max_length=200, blank=True)
    twitter_link = models.URLField(max_length=200, blank=True)
    youtube_link = models.URLField(max_length=200, blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    

    def __str__(self):
        return self.website_name
    
#about     
class About(models.Model):
    name = models.CharField(max_length=255,default='About Us')
    title      = models.CharField(max_length=250, blank=True)
    meta_description = models.TextField(max_length=300,blank=True)
    meta_keywords    = models.TextField(max_length=300,blank=True)
    bg_banner = models.ImageField(upload_to='photos/banner', blank=True)
    about_img = models.ImageField(upload_to='about/%Y/%m/%d/',blank=True)
    heading = models.CharField(max_length=255, blank=True)
    content = RichTextUploadingField(null=True, blank=True)
    button_name = models.CharField(max_length=255,default='Read More')
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
       
    def __str__(self):
        return self.name 
      
#Objective    
class Objective(models.Model):
    about = models.ForeignKey(About, on_delete=models.CASCADE)
    title_name      = models.CharField(max_length=350)
    heading = models.CharField(max_length=255, blank=True)
    photo = models.ImageField(upload_to='about/%Y/%m/%d/',blank=True)
    content = RichTextUploadingField(null=True, blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    def __str__(self):
        return self.title_name 
    
    
#Banner model     
class HeroBanner(models.Model):
    banner_name = models.CharField(max_length=355)
    title      = models.CharField(max_length=250, blank=True)
    meta_description = models.TextField(max_length=300,blank=True)
    meta_keywords    = models.TextField(max_length=300,blank=True)
    heading_1 = models.CharField(max_length=355, default='Property Dekhoge',blank=True)
    heading_2 = models.CharField(max_length=355, default='Find Your Dream Home',blank=True)
    banner = models.ImageField(upload_to='banner/%Y/%m/%d/',blank=True)
    imgage = models.ImageField(upload_to='banner/%Y/%m/%d/',blank=True)
    description = models.TextField(max_length=500, blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    def __str__(self):
        return self.banner_name 
    
    
class PageBanner(models.Model):
    pagename = models.CharField(max_length=100)
    title      = models.CharField(max_length=250, blank=True)
    meta_description = models.TextField(max_length=300,blank=True)
    meta_keywords    = models.TextField(max_length=300,blank=True)
    bg_banner = models.ImageField(upload_to='photos/banner/%Y/%m/%d/', blank=True)
    title= models.CharField(max_length=100, default='Banner Title')
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    

    class Meta:
        verbose_name = 'Page Banner'
        verbose_name_plural = 'Page Banners'

    def __str__(self):
        return self.pagename  
    
    
#Developerpage     
class DeveloperPage(models.Model):
    name = models.CharField(max_length=255,default='Developer')
    title      = models.CharField(max_length=250, blank=True)
    meta_description = models.TextField(max_length=300,blank=True)
    meta_keywords    = models.TextField(max_length=300,blank=True)
    bg_banner = models.ImageField(upload_to='photos/banner', blank=True)
    image = models.ImageField(upload_to='pages/%Y/%m/%d/',blank=True)
    heading = models.CharField(max_length=255, blank=True)
    content = RichTextUploadingField(null=True, blank=True)
    button_name = models.CharField(max_length=255,default='Read More')
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
       
    def __str__(self):
        return self.name  
    
#Projectpage    
class ProjectPage(models.Model):
    name = models.CharField(max_length=255,default='Project')
    title      = models.CharField(max_length=250, blank=True)
    meta_description = models.TextField(max_length=300,blank=True)
    meta_keywords    = models.TextField(max_length=300,blank=True)
    bg_banner = models.ImageField(upload_to='photos/banner', blank=True)
    image = models.ImageField(upload_to='pages/%Y/%m/%d/',blank=True)
    heading = models.CharField(max_length=255, blank=True)
    content = RichTextUploadingField(null=True, blank=True)
    button_name = models.CharField(max_length=255,default='Read More')
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
       
    def __str__(self):
        return self.name   
    
#Agentpage    
class AgentPage(models.Model):
    name = models.CharField(max_length=255,default='Project')
    title      = models.CharField(max_length=250, blank=True)
    meta_description = models.TextField(max_length=300,blank=True)
    meta_keywords    = models.TextField(max_length=300,blank=True)
    bg_banner = models.ImageField(upload_to='photos/banner', blank=True)
    image = models.ImageField(upload_to='pages/%Y/%m/%d/',blank=True)
    heading = models.CharField(max_length=255, blank=True)
    content = RichTextUploadingField(null=True, blank=True)
    button_name = models.CharField(max_length=255,default='Read More')
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
       
    def __str__(self):
        return self.name
    
#PrivacyPolicy   
class PrivacyPolicy(models.Model):
    name = models.CharField(max_length=255,default='Project')
    title      = models.CharField(max_length=250, blank=True)
    meta_description = models.TextField(max_length=300,blank=True)
    meta_keywords    = models.TextField(max_length=300,blank=True)
    bg_banner = models.ImageField(upload_to='photos/banner', blank=True)
    image = models.ImageField(upload_to='pages/%Y/%m/%d/',blank=True)
    heading = models.CharField(max_length=255, blank=True)
    content = RichTextUploadingField(null=True, blank=True)
    button_name = models.CharField(max_length=255,default='Read More')
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
       
    def __str__(self):
        return self.name                           