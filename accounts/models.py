from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.db.models.fields.related import ForeignKey, OneToOneField
from ckeditor_uploader.fields import RichTextUploadingField
from django_ckeditor_5.fields import CKEditor5Field
from accounts.managers import UserManager
from django.utils import timezone
from django.urls import reverse

# Create your models here.
STATUS = (
    (0,"Draft"),
    (1,"Publish")
)

class User(AbstractBaseUser):

    ROLE_CHOICE = (
        ('MyAdmin', 'MyAdmin'),
        ('Vendor', 'Vendor'),
        ('Customer', 'Customer'),
    )
    first_name      = models.CharField(max_length=50)
    last_name       = models.CharField(max_length=50)
    username        = models.CharField(max_length=150, unique=True)
    email           = models.EmailField(max_length=100, unique=True)
    phone_number    = models.CharField(max_length=12, blank=True)
    # role = models.PositiveSmallIntegerField(choices=ROLE_CHOICE, blank=True, null=True)
    role = models.CharField(max_length=60, choices=ROLE_CHOICE, blank=True, null=True)

    # required
    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(auto_now_add=True)
    created_date = models.DateTimeField(auto_now_add=True)
    modified_date = models.DateTimeField(auto_now=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=False)
    is_superadmin = models.BooleanField(default=False)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username', 'first_name', 'last_name']

    objects = UserManager()
    
    def generate_username(self):
        base_username = self.email.split('@')[0]
        username = base_username
        num = 1

        # Keep incrementing the number until a unique username is found
        while User.objects.filter(username=username).exists():
            username = f"{base_username}_{num}"
            num += 1

        return username
    
    def save(self, *args, **kwargs):
        # Auto-generate the username if it's not provided
        if not self.username:
            self.username = self.generate_username()
        super().save(*args, **kwargs)

    def full_name(self):
        return f'{self.first_name} {self.last_name}'

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return self.is_admin

    def has_module_perms(self, add_label):
        return True
    
    def get_role(self):
        if self.role == 'Myadmin':
            user_role = 'MyAdmin'
        elif self.role == 'Vendor':
            user_role = 'Vendor'
        elif self.role == 'Customer':
            user_role = 'Customer'    
        return user_role
         
    
    
class UserProfile(models.Model):
    user = OneToOneField(User, on_delete=models.CASCADE, blank=True, null=True)
    profile_picture = models.ImageField(upload_to='users/profile_pictures', blank=True, null=True)
    bio = RichTextUploadingField(max_length=350, blank=True, null=True)
    address = models.CharField(max_length=250, blank=True, null=True)
    country = models.CharField(max_length=15, blank=True, null=True)
    state = models.CharField(max_length=15, blank=True, null=True)
    city = models.CharField(max_length=15, blank=True, null=True)
    pin_code = models.CharField(max_length=6, blank=True, null=True)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)

    # def full_address(self):
    #     return f'{self.address_line_1}, {self.address_line_2}'

    def __str__(self):
        return self.user.email 
    

class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    author_name = models.CharField(max_length=50)
    author_slug = models.SlugField(max_length=100, blank=True, null=True, unique=True)
    # content = RichTextUploadingField(blank=True, null=True)
    content = CKEditor5Field(config_name='extends',blank=True, null=True)
    # content = CKEditor5Field('Content', config_name='default',blank=True, null=True)
    designation = models.CharField(max_length=255,blank=True)
    is_approved = models.BooleanField(default=False)
    created_on = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.author_name 


class EnqEmailSetting(models.Model):
    status_choice=(
        ('active', 'Active'),
        ('inactive', 'Inactive')
    )
    name = models.CharField(max_length=100, help_text="Email Name")
    enqmail = models.EmailField(max_length=200, help_text="Enquiry Mail Add", blank=True)
    status = models.CharField(max_length=50, choices=status_choice, default='inactive', null=True)
    
    def __str__(self):
        return "Admin Receiving Email" 