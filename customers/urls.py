from django.urls import path
from . import views

urlpatterns = [
    path('', views.customer, name='customer'),
    path('dashboard/', views.customer, name='cdashboard'),
    path('edit-profile/', views.edit_cprofile, name='edit_cprofile'),
    path('change-password/', views.change_cpassword, name='change_cpassword'),
    path('enquiry-detail/<int:pk>/', views.enquiry_cdetail, name='enquiry_cdetail'),
    # path('<slug:service_slug>/', views.service_detail, name='service_detail'),
    # path('inquiry', views.inquiry, name='inquiry'),
    # path('sector/<slug:sector_slug>/', views.jobpost, name='jobs_by_sector'),
]