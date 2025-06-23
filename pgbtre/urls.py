"""pgbtre URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.models import Group
from . import views
# admin.site.unregister(Group)
admin.site.site_header = "Property Dekhoge"
admin.site.site_title = "Property Dekhoge"
admin.site.index_title = "Welcome to Property Dekhoge"
urlpatterns = [
    path('', views.home, name='home'),
    path('about-us/', views.about, name='about'),
    path('developers/', views.developerlist, name='developer'),
    path('projects/', views.projectlist, name='projects'),
    path('agents/', views.agentlist, name='agents'),
    path('privacy-policy/', views.privacypolicy, name='privacypolicy'),
    path('contact-us/', views.contact, name='contact'),
    path('pages', include('pages.urls')),
    path('', include('listings.urls')),
    path('accounts/', include('accounts.urls')),
    path('contacts/', include('contacts.urls')),
    path('realtor/', include('realtors.urls')),
    path('user/', include('customers.urls')),
    path('myadmin/', include('myadmin.urls')),
    path('admin/', admin.site.urls),
    path('ckeditor/', include('ckeditor_uploader.urls')),
    path("ckeditor5/", include('django_ckeditor_5.urls')),
    # path("upload/", custom_upload_function, name="custom_upload_file"),
    # path("ckeditor5/", include('django_ckeditor_5.urls'), name="ck_editor_5_upload_file"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
