from django.urls import path

from . import views

urlpatterns = [
    path('listings/', views.listings, name='listings'),
    # path('<int:listing_id>', views.listing, name='listing'),
    path('agent/<slug:realtor_slug>/', views.agent, name='agent'),
    path('developer/<slug:developer_slug>/', views.developer, name='developer'),
    path('project/<slug:project_slug>/', views.project, name='project'),
    path('property-detail/<slug:city_slug>/<slug:listing_slug>/', views.listing, name='listing'),
    path('<slug:city_slug>-property/', views.listings, name='property_by_city'),
    path('property-for-sale-in-<slug:locality_slug>/', views.listings, name='property_by_locality'), 
    path('search', views.search, name='search'),
]