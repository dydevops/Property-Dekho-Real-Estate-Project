from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from accounts.decorators import check_role_customer
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

# def get_customer(request):
#     customer = User.objects.get(user=request.user)
#     return customer

@login_required(login_url='login')
@user_passes_test(check_role_customer)
def change_cpassword(request):
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
                return redirect('change_cpassword')
            else:
                messages.error(request, 'Please enter valid current password')
                return redirect('change_cpassword')
        else:
            messages.error(request, 'Password does not match!')
            return redirect('change_cpassword')
    return render(request, 'customers/change_password.html')
  
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def edit_cprofile(request):
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
            return redirect('edit_cprofile')
    else:
        user_form = UserInfoForm(instance=request.user)
        profile_form = UserProfileForm(instance=userprofile)
        
    context = {
        'user_form': user_form,
        'profile_form': profile_form,
        # 'userprofile': userprofile,
    }
    return render(request, 'customers/edit_profile.html', context)
    
    
@login_required(login_url='login')
@user_passes_test(check_role_customer)
def customer(request):
    listingenquiry = ListingEnquiry.objects.filter(customer=request.user).order_by('-created_on')
    # listingenquiry = ListingEnquiry.objects.filter(listing__realtor=get_vendor(request)).order_by('-created_on')  

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
    return render(request, 'customers/dashboard.html', context)


@login_required(login_url='login')
@user_passes_test(check_role_customer)
def enquiry_cdetail(request, pk=None):
     enquiry = get_object_or_404(ListingEnquiry, pk=pk)
   
     context ={
         'enquiry': enquiry,

     }
     return render(request, 'customers/enquiry_details.html', context)

