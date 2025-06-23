from django.db import models
from datetime import datetime
from django.utils.timezone import now
from django.utils import timezone
from django.urls import reverse
from django.utils.text import slugify
from ckeditor_uploader.fields import RichTextUploadingField
from accounts.utils import send_notification
from accounts.models import User, UserProfile
from datetime import time, date, datetime
# Create your models here.
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class Realtor(models.Model):
  user = models.OneToOneField(User, on_delete=models.CASCADE)
  name = models.CharField(max_length=200)
  slug            = models.SlugField(max_length=400, unique=True,null=True,blank=True)
  photo = models.ImageField(upload_to='photos/%Y/%m/%d/',blank=True, null=True)
  description = RichTextUploadingField(blank=True, null=True)
  phone = models.CharField(max_length=20,blank=True, null=True)
  email = models.EmailField(max_length=150,blank=True, null=True)
  agent_rera = models.CharField(max_length=360,blank=True, null=True)
  rera_link = models.URLField(max_length=600,null=True, blank=True)
  is_mvp = models.BooleanField(default=False)
  hire_date = models.DateTimeField(default=datetime.now, blank=True)
  is_approved = models.BooleanField(default=False)
  created_on = models.DateTimeField(default=timezone.now)
  updated_on = models.DateTimeField(auto_now=True)
  status = models.IntegerField(choices=STATUS, default=0)
  
  class Meta:
      verbose_name = 'Agent'
      verbose_name_plural = 'Agents'
      ordering = ['-created_on']
      
  
  def get_url(self):
            return reverse('agent', args=[self.slug])
  
  def __str__(self):
    return self.name

  def save(self, *args, **kwargs):
        if self.pk is not None:
            # Update
            orig = Realtor.objects.get(pk=self.pk)
            if orig.is_approved != self.is_approved:
                mail_template = 'emails/admin_approval_email.html'
                context = {
                    'user': self.user,
                    'is_approved': self.is_approved,
                    'to_email': self.user.email,
                }
                if self.is_approved == True:
                    # Send notification email
                    mail_subject = "Congratulations! Your Agent ID has been approved."
                    send_notification(mail_subject, mail_template, context)
                else:
                    # Send notification email
                    mail_subject = "We're sorry! You are not eligible for publishing your listing on our marketplace."
                    send_notification(mail_subject, mail_template, context)
        return super(Realtor, self).save(*args, **kwargs)


  
  
class EmailSetting(models.Model):
    status_choice=(
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )
    realtor = models.ForeignKey(Realtor, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, help_text="Email Name")
    enqmail = models.EmailField(max_length=200, help_text="Enquiry Mail Add", blank=True)
    status = models.CharField(max_length=50, choices=status_choice, default='inactive', null=True)
    
    # class Meta:
    #     verbose_name = 'Agents Email'
    #     verbose_name_plural = '2. Agents Email'
    #     ordering = ['-created_on']
        
    def __str__(self):
        return "Receiving Email"  