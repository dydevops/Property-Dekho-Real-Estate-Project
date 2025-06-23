from django.db import models
from datetime import datetime
# from django.conf import settings
from django.utils.timezone import now
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from django_ckeditor_5.fields import CKEditor5Field
import uuid

# Create your models here.
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)
class Country(models.Model):
    country_name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=600,unique=True,blank=True, null=True)
    country_pic= models.ImageField(upload_to='country/%Y/%m/%d/',null=True,blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        verbose_name = 'Country'
        verbose_name_plural = '1. Countries'
        ordering = ['-created_on']
  
    # @property
    # def get_instance(self):
    #     return self
    def save(self, *args, **kwargs):
        self.full_clean()  # Runs the custom validation
        if not self.slug:
            self.slug = slugify(f"{self.country_name}")
        super(Country, self).save(*args, **kwargs)
        
    def __str__(self):
        return self.country_name
    
class State(models.Model):
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    state_name = models.CharField(max_length=100,unique=True)
    slug = models.SlugField(max_length=600,unique=True,blank=True, null=True)
    state_pic= models.ImageField(upload_to='state/%Y/%m/%d/',null=True,blank=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        verbose_name = 'State'
        verbose_name_plural = '2. States'
        ordering = ['-created_on']
        
    def save(self, *args, **kwargs):
        self.full_clean()  # Runs the custom validation
        if not self.slug:
            self.slug = slugify(f"{self.state_name}")
        super(State, self).save(*args, **kwargs)    
        
    def __str__(self):
        return self.state_name
    
class Developer(models.Model):
    developer_name = models.CharField(max_length=350)
    slug = models.SlugField(max_length=450, blank=True, null=True, unique=True)
    description = RichTextUploadingField(blank=True, null=True)
    website_url = models.URLField(max_length=650,blank=True)
    photo = models.ImageField(upload_to='developer/%Y/%m/%d/', blank=True)
    is_approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        verbose_name = 'Developer'
        verbose_name_plural = '3. Developers'
        ordering = ['-created_on']
        
    def save(self, *args, **kwargs):
        self.full_clean()  # Runs the custom validation
        if not self.slug:
            self.slug = slugify(f"{self.developer_name}")
        super(Developer, self).save(*args, **kwargs)      
        
    def get_url(self):
         return reverse('developer', args=[self.slug])    
    
    def __str__(self):
        return self.developer_name
    
class Project(models.Model):
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE,blank=True, null=True,)
    project_name = models.CharField(max_length=350)
    slug = models.SlugField(max_length=450, blank=True, null=True, unique=True)
    description = RichTextUploadingField(blank=True, null=True)
    website_url = models.URLField(max_length=650,blank=True)
    photo = models.ImageField(upload_to='project/%Y/%m/%d/', blank=True)
    project_rera = models.CharField(max_length=360,blank=True, null=True)
    rera_link = models.URLField(max_length=600,null=True, blank=True)
    qrcode = models.ImageField(upload_to='project/qrcode/%Y/%m/%d/',null=True,blank=True)
    is_approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=0)
    
    class Meta:
        verbose_name = 'Project'
        verbose_name_plural = '4. Projects'
        ordering = ['-created_on']
        
    def save(self, *args, **kwargs):
        self.full_clean()  # Runs the custom validation
        if not self.slug:
            self.slug = slugify(f"{self.project_name}")
        super(Project, self).save(*args, **kwargs)    
        
    def get_url(self):
         return reverse('project', args=[self.slug])      
    
    def __str__(self):
        return self.project_name     
