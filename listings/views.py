from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.contrib import messages,auth
from django.core.mail import send_mail
from accounts.models import UserProfile,EnqEmailSetting
from contacts.forms import ListingEnquiryForm
from contacts.models import ListingEnquiry
from realtors.models import Realtor,EmailSetting
from pages.models import PageBanner
from .choices import price_choices, bedroom_choices, state_choices
from listings.models import City,Listing,ListingCategory,Configuration,Possession,Locality,ListingGallery,Amenities,FloorPlan
from project.models import State,Country,Developer,Project
from django.db.models import Q


def developer(request,developer_slug):
    # category = ProductCategory.objects.filter(status=1).order_by('-created_on')[0:9]
    developer = get_object_or_404(Developer, slug=developer_slug)
    listings = Listing.objects.filter(developer_id=developer.id,status=1).order_by('created_on')
    banner = PageBanner.objects.filter(status=1).first()
    # slides = Slide.objects.filter(status=1).order_by('created_on')[0:3]
   
    context = {
        'developer': developer,
        'listings': listings,
        'banner': banner,
        'cities': City.objects.all(),
        'categories': ListingCategory.objects.all(),
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'configurations': Configuration.objects.all(),
        'possessions': Possession.objects.all(),
    }

    return render(request, 'main/developer.html',context)
  
  
def project(request,project_slug):
    # category = ProductCategory.objects.filter(status=1).order_by('-created_on')[0:9]
    project = get_object_or_404(Project, slug=project_slug)
    listings = Listing.objects.filter(project_id=project.id,status=1).order_by('created_on')
    banner = PageBanner.objects.filter(status=1).first()
    # slides = Slide.objects.filter(status=1).order_by('created_on')[0:3]
   
    context = {
        'project': project,
        'listings': listings,
        'banner': banner,
        'cities': City.objects.all(),
        'categories': ListingCategory.objects.all(),
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'configurations': Configuration.objects.all(),
        'possessions': Possession.objects.all(),
    }

    return render(request, 'main/project.html',context) 
  
  
def agent(request,realtor_slug):
    # category = ProductCategory.objects.filter(status=1).order_by('-created_on')[0:9]
    realtor = get_object_or_404(Realtor, slug=realtor_slug)
    listings = Listing.objects.filter(realtor_id=realtor.id,status=1).order_by('created_on')
    banner = PageBanner.objects.filter(status=1).first()
    # slides = Slide.objects.filter(status=1).order_by('created_on')[0:3]
   
    context = {
        'realtor': realtor,
        'listings': listings,
        'banner': banner,
        'cities': City.objects.all(),
        'categories': ListingCategory.objects.all(),
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'configurations': Configuration.objects.all(),
        'possessions': Possession.objects.all(),
    }

    return render(request, 'main/realtor.html',context)     



def listings(request,city_slug=None,locality_slug=None):
  cities = None
  localities = None
  listings = None
  if city_slug != None:
    cities  = get_object_or_404(City, slug=city_slug)
    listings = Listing.objects.filter(city=cities,status=1).order_by('-created_on')
    banner = PageBanner.objects.filter(status=1).first()
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    
  elif locality_slug != None:
    localities  = get_object_or_404(Locality, slug=locality_slug)
    listings = Listing.objects.filter(locality=localities,status=1).order_by('-created_on')
    banner = PageBanner.objects.filter(status=1).first()
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page) 
    print('listings') 
  
  else:
    listings = Listing.objects.order_by('-created_on').filter(status=1)
    banner = PageBanner.objects.filter(status=1).first()
    paginator = Paginator(listings, 6)
    page = request.GET.get('page')
    paged_listings = paginator.get_page(page)
    
    # process = Process.objects.filter(status=1).order_by('created_on')[0:3]
    # testimonials = Testimonial.objects.filter(status=1).order_by('-created_on')
    # homepage = Homepage.objects.filter(status=1).first()

  context = {
    'listings': paged_listings,
    'banner': banner,
    'cities': City.objects.all(),
    'categories': ListingCategory.objects.all(),
    'bedroom_choices': bedroom_choices,
    'price_choices': price_choices,
    'configurations': Configuration.objects.all(),
    'possessions': Possession.objects.all(),
  }

  return render(request, 'main/listings.html', context)

def listing(request, city_slug,listing_slug):
  listing = get_object_or_404(Listing,city__slug=city_slug, slug=listing_slug)
  # Get the product gallery
  listing_gallery = ListingGallery.objects.filter(listing_id=listing.id)
  amenities = Amenities.objects.filter(listing_id=listing.id)
  floorplans = FloorPlan.objects.filter(listing_id=listing.id)
  # Retrieve similar properties based on the city
  similar_properties = Listing.objects.filter(city=listing.city).exclude(id=listing.id)[0:3]
  featuredlist = Listing.objects.filter(status=1,is_featured=True).order_by('-created_on')[0:3]
  email_setting = EnqEmailSetting.objects.all().first()
  vqnemail=listing.realtor.user.email
  realtor = listing.realtor
  print(vqnemail)
  if email_setting and email_setting.enqmail:
        # Use enqmail if it's not empty
        vemail = email_setting.enqmail
    # elif vendor.user:
    #     # Use the email from the associated User if available
    #     vemail = vendor.user.email
  else:
      # Fallback to a default email or handle as needed
      avemail = "darpankario@gmail.com"
  # print(vendor) 
  if request.method == 'POST':
      form = ListingEnquiryForm(request.POST,request.FILES)
      if form.is_valid():
          listing_name = form.cleaned_data['listing_name']
          listing_url = form.cleaned_data['listing_url']
          full_name = form.cleaned_data['full_name']
          email = form.cleaned_data['email']
          phone_no = form.cleaned_data['phone_no']
          city = form.cleaned_data['city']
          requirement = form.cleaned_data['requirement']
          enquire = ListingEnquiry(listing_name=listing_name, listing_url=listing_url, full_name=full_name, email=email, phone_no=phone_no, city=city, requirement=requirement)
          enquire = form.save(commit=False)
          if request.user.is_authenticated:
              enquire.customer = request.user
          else:
              enquire.customer = None
          enquire.realtor = realtor
          enquire.listing = listing
          enquire.save()
          current_site = get_current_site(request)
          # feedback = form.save(commit=False)
          data = {
              'listing_name': listing_name, 
              'listing_url': listing_url,
              'full_name': full_name,
              'email': email,
              'phone_no': phone_no,
              'city': city,
              'realtor': listing.realtor,
              'realtor_email': listing.realtor.user.email,
              'domain': current_site,
              'list_link': listing.slug,
              'list_city': listing.city,
              'requirement': requirement,
          }
          subject = "New Listing Enquiry from {}".format(enquire.full_name)
          msg_html = render_to_string('emails/listing_enquiry_template.html', data)
          customer_html = render_to_string('emails/thankyou_email.html', data)
          enquire.save()
          send_mail(
              subject,
              email,
              phone_no,
              [vemail,vqnemail],
              # [feedback.email],
              html_message=msg_html,
          )
          # Send confirmation email to the vendor
          # vendor_email = feedback_instance.vendor.user.email
          send_mail(
              'Thank You for Your Feedback',
              '',
              'dharmendrayadav076@gmail.com',  # Replace with your email address
              [enquire.email],
              # fail_silently=False,
              html_message=customer_html,
          )
          # return redirect('/')  # Redirect to the vendor detail page
          messages.success(request, 'Your Message has been send sucessfully!')
          return redirect('listing',city_slug,listing_slug)
  else:
      form = ListingEnquiryForm()
      # mv_email = EmailSetting.objects.all().filter(vendor=vendor).first()
      # vmemail= mv_email.enqmail

  context = {
    'listing': listing,
    'listing_gallery': listing_gallery,
    'form': form,
    'realtor': realtor,
    'similar_properties': similar_properties,
    'featuredlist': featuredlist,
    'amenities': amenities ,
    'floorplans': floorplans,
  }

  return render(request, 'main/listing.html', context)



def search(request):
  queryset_list = Listing.objects.order_by('-list_date')
  banner = PageBanner.objects.filter(status=1).first()
  
  if 'tab' in request.GET:
       tab = request.GET['tab']
       if tab in ['Buy', 'Rent']:
           queryset_list = queryset_list.filter(listing_type=tab)

  # Keywords
  if 'keywords' in request.GET:
    keywords = request.GET['keywords']
    if keywords:
      queryset_list = queryset_list.filter(
        Q(description__icontains=keywords)|
        Q(title__icontains=keywords)| 
        Q(configuration__name__icontains=keywords)|
        Q(category__category_name__icontains=keywords)|
        Q(developer__developer_name__icontains=keywords)|
        Q(project__project_name__icontains=keywords)|
        Q(realtor__name__icontains=keywords)|
        Q(locality__local_name__icontains=keywords)|
        Q(possession__name__icontains=keywords)|
        Q(listing_type__icontains=keywords)|
        Q(state__state_name__icontains=keywords)
      )

  # City
  if 'city' in request.GET:
    city = request.GET['city']
    if city:
      queryset_list = queryset_list.filter(city__city_name=city)

  # category
  if 'category' in request.GET:
    category = request.GET['category']
    if category:
      queryset_list = queryset_list.filter(category__category_name=category)
      
   # configuration
  if 'configuration' in request.GET:
    configuration = request.GET['configuration']
    if configuration:
      queryset_list = queryset_list.filter(configuration__name=configuration)
      
    # configuration
  if 'possession' in request.GET:
    possession = request.GET['possession']
    if possession:
      queryset_list = queryset_list.filter(possession__name=possession)        

  # Bedrooms
  if 'bedrooms' in request.GET:
    bedrooms = request.GET['bedrooms']
    if bedrooms:
      queryset_list = queryset_list.filter(bedrooms__lte=bedrooms)

  # Price
  if 'price' in request.GET:
    price = request.GET['price']
    if price:
      queryset_list = queryset_list.filter(price__lte=price)

  context = {
    'banner': banner,
    'state_choices': state_choices,
    'bedroom_choices': bedroom_choices,
    'price_choices': price_choices,
    'listings': queryset_list,
    'cities': City.objects.all(),
    'states': State.objects.all(),
    'categories': ListingCategory.objects.all(),
    'configurations': Configuration.objects.all(),
    'possessions': Possession.objects.all(),
    'values': request.GET,
  }

  return render(request, 'main/listings.html', context)
