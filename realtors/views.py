from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.decorators import check_role_vendor
from django.contrib import messages
from django.core.paginator import EmptyPage, PageNotAnInteger, Paginator
from django.db.models import Q
from accounts.models import User, UserProfile
from accounts.forms import UserForm,UserProfileForm,UserInfoForm
from contacts.models import Contact,ListingEnquiry
from listings.models import City,State,ListingCategory,Configuration,Possession,Locality,ListingGallery,Listing
from realtors.models import Realtor
from realtors.forms import VendorForm
# Create your views here.
# def staff(request):
#     html = "<html><body>Hello This is My Staff</body></html>"
#     return HttpResponse(html)

# @login_required(login_url='login')
# @user_passes_test(check_role_vendor)  
# def agent(request):
#     # enquiry = Services_enquiry.objects.all().order_by('-id')
#     # jobs = Job.objects.filter(status=1).order_by('-created_on')[0:8]
#     # feedback = Feedback.objects.all().order_by('-id')
#     # applicants = Applicant.objects.all().order_by('-id')
#     # enquiry_count = enquiry.count()
#     # job_count = jobs.count()
#     # feedback_count = feedback.count()
#     # applicant_count = applicants.count()

#     # context = {
#     #     'enquiry': enquiry,
#     #     'enquiry_count': enquiry_count,
#     #     'applicant_count': applicant_count,
#     #     'feedback_count': feedback_count,
#     #     'job_count': job_count,
#     # }
#     return render(request, 'agents/dashboard.html')
#     # return render(request, 'myadmin/adhome.html',context)

def get_vendor(request):
    realtor = Realtor.objects.get(user=request.user)
    return realtor

@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def change_vpassword(request):
    if request.method == 'POST':
        current_password = request.POST['current_password']
        new_password = request.POST['new_password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.get(username__exact=request.user.username)

        if new_password == confirm_password:
            success = user.check_password(current_password)
            if success:
                user.set_password(new_password)
                user.save()
                # auth.logout(request)
                messages.success(request, 'Password updated successfully.')
                return redirect('change_vpassword')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_vpassword')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_vpassword')
    return render(request, 'agents/change_password.html')
  
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def edit_vprofile(request):
    userprofile = get_object_or_404(UserProfile, user=request.user)
    if request.method == 'POST':
        user_form = UserInfoForm(request.POST, instance=request.user)
        profile_form = UserProfileForm(request.POST, request.FILES, instance=userprofile)
        if user_form.is_valid() and profile_form.is_valid():
            user=user_form.save()
            # user.set_password(user.password)
            user.save()
            profile=profile_form.save(commit=False)
            # profile.address=profile_form.cleaned_data['address']
            # profile.country=profile_form.cleaned_data['country']
            # profile.state=profile_form.cleaned_data['state']
            # profile.city=profile_form.cleaned_data['city']
            # profile.pin_code=profile_form.cleaned_data['pin_code']
            profile.save()
            messages.success(request, 'Your profile has been updated.')
            return redirect('edit_vprofile')
    else:
        user_form = UserInfoForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        # 'userprofile': userprofile,
    }
    return render(request, 'agents/edit_profile.html', context)
    
# @login_required(login_url='login')
# @user_passes_test(check_role_vendor)
# def agent(request):
#   # enquiry = ListingEnquiry.objects.order_by('-created_on')
#   realtor = Realtor.objects.get(user=request.user)
#   # vendor=enquiry.realtor
#   listingenquiry = ListingEnquiry.objects.filter(listing__realtor=realtor)
#   # listingenquiry = ListingEnquiry.objects.filter(listingenquiry__realtor=get_vendor(request))
  
#   # listingenquiry = ListingEnquiry.objects.order_by('-created_on')
# #   listingenquiry = ListingEnquiry.objects.order_by('-created_on').filter(user_id=request.user.id)
#   paginator = Paginator(listingenquiry, 1)
#   page = request.GET.get('page')
#   paged_enquiry = paginator.get_page(page)

#   context = {
#     'listingenquiry': paged_enquiry,
#   }
#   return render(request, 'agents/dashboard.html', context)
@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def agent(request):
    listingenquiry = ListingEnquiry.objects.filter(listing__realtor=get_vendor(request)).order_by('-created_on')  # Efficiently fetch and order in a single query

    # Pagination configuration
    paginator = Paginator(listingenquiry, 6)  # Display 5 items per page
    page = request.GET.get('page')

    try:
        paged_enquiry = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page
        paged_enquiry = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g., 9999), deliver last page of results
        paged_enquiry = paginator.page(paginator.num_pages)

    context = {
        'listingenquiry': paged_enquiry,
    }
    return render(request, 'agents/dashboard.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vproperty(request):
  listings = Listing.objects.filter(status=1,realtor=get_vendor(request)).order_by('-created_on')
  paginator = Paginator(listings, 6)
  page = request.GET.get('page')
  paged_listings = paginator.get_page(page)

  context = {
    'listings': paged_listings,
  }
  return render(request, 'agents/my_properties.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def enquiry_vdetail(request, pk=None):
     enquiry = get_object_or_404(ListingEnquiry, pk=pk)
   
     context ={
         'enquiry': enquiry,

     }
     return render(request, 'agents/enquiry_details.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_vendor)
def vprofile(request):
    vendor = get_object_or_404(Realtor, user=request.user)
    if request.method == 'POST':
        vendor_form = VendorForm(request.POST, request.FILES, instance=vendor)
        if vendor_form.is_valid():
            vendor_form.save()
            messages.success(request, 'Settings updated.')
            return redirect('vprofile')
        else:
            print(vendor_form.errors)
    else:
        vendor_form = VendorForm(instance=vendor)

    context = {
        'vendor_form': vendor_form,
        'vendor': vendor,
    }
    return render(request, 'agents/vprofile.html', context)