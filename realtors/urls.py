from django.urls import path
from . import views

urlpatterns = [
    path('', views.agent, name='agent'),
    path('dashboard/', views.agent, name='vdashboard'),
    path('edit-profile/', views.edit_vprofile, name='edit_vprofile'),
    path('vprofile/', views.vprofile, name='vprofile'),
    path('change-password/', views.change_vpassword, name='change_vpassword'),
    path('enquiry-detail/<int:pk>/', views.enquiry_vdetail, name='enquiry_vdetail'),
    path('my-property/', views.vproperty, name='vproperty'),
    # path('edit-profile/', views.edit_staffprofile, name='edit_staffprofile'),
    # path('change-password/', views.change_staffpassword, name='change_staffpassword'),
    # path('<slug:service_slug>/', views.service_detail, name='service_detail'),
    # path('inquiry', views.inquiry, name='inquiry'),
    # path('sector/<slug:sector_slug>/', views.jobpost, name='jobs_by_sector'),
]