from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from listings.choices import price_choices, bedroom_choices, state_choices

from listings.models import Listing,City,State,ListingCategory,Configuration,Possession
from realtors.models import Realtor


def myDashboard(request):
    html = "<html><body>My Pages</body></html>"
    return HttpResponse(html)

# def index(request):
#     listings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]

#     context = {
#         'listings': listings,
#         'state_choices': state_choices,
#         'bedroom_choices': bedroom_choices,
#         'price_choices': price_choices,
#         'cities': City.objects.all(),
#         'states': State.objects.all(),
#         'categories': ListingCategory.objects.all(),
#         'configurations': Configuration.objects.all(),
#         'possessions': Possession.objects.all(),
#     }

#     return render(request, 'pages/index.html', context)


# def about(request):
#     # Get all realtors
#     realtors = Realtor.objects.order_by('-hire_date')

#     # Get MVP
#     mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

#     context = {
#         'realtors': realtors,
#         'mvp_realtors': mvp_realtors
#     }

#     return render(request, 'pages/about.html', context)
