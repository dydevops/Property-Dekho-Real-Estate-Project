from django.shortcuts import render,redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.db.models import Q
from listings.choices import price_choices, bedroom_choices, state_choices
from listings.models import Listing,City,State,ListingCategory,Configuration,Possession
from realtors.models import Realtor
from project.models import Project,Developer
from pages.models import About,Objective,HeroBanner,DeveloperPage,ProjectPage,AgentPage,PrivacyPolicy
from contacts.forms import FeedbackForm
from contacts.models import Feedback,Contact
from accounts.models import UserProfile,EnqEmailSetting
from django.contrib import messages,auth
from django.core.mail import send_mail
from django.template.loader import render_to_string

def home(request):
    listings = Listing.objects.order_by('-created_on').filter(status=1)
    mycities = City.objects.filter(is_featured=True,status=1).order_by('created_on')[:3]
    propertytype = ListingCategory.objects.filter(is_featured=True,status=1).order_by('created_on')[:4]
    mylistings = Listing.objects.order_by('-list_date').filter(is_published=True)[:3]
    banner = HeroBanner.objects.filter(status=1).first()

    context = {
        'listings': listings,
        'hero': banner,
        'mylistings': mylistings,
        'state_choices': state_choices,
        'bedroom_choices': bedroom_choices,
        'price_choices': price_choices,
        'mycities': mycities,
        'propertytype': propertytype,
        'cities': City.objects.all(),
        'states': State.objects.all(),
        'categories': ListingCategory.objects.all(),
        'configurations': Configuration.objects.all(),
        'possessions': Possession.objects.all(),
    }

    return render(request, 'main/home.html', context)


def about(request):
    # Get all realtors
    projects = Project.objects.filter(status=1).order_by('-created_on')
    about = About.objects.filter(status=1).first()
    aboutdt = Objective.objects.filter(about_id=about.id).order_by('created_on')
    # Get MVP
    mvp_realtors = Realtor.objects.all().filter(is_mvp=True)

    context = {
        'projects': projects,
        'about': about,
        'aboutdt': aboutdt,
        'mvp_realtors': mvp_realtors,
    }

    return render(request, 'main/about.html', context)


def developerlist(request):
    # Get all realtors
    developers = Developer.objects.filter(status=1).order_by('-created_on')
    page = DeveloperPage.objects.filter(status=1).first()

    context = {
        'page': page,
        'developers': developers,
    }

    return render(request, 'main/developer_list.html', context)

def projectlist(request):
    # Get all realtors
    projects = Project.objects.filter(status=1).order_by('-created_on')
    page = ProjectPage.objects.filter(status=1).first()

    context = {
        'page': page,
        'projects': projects,
    }

    return render(request, 'main/project_list.html', context)

def agentlist(request):
    # Get all realtors
    realtors = Realtor.objects.filter(status=1).order_by('-created_on')
    page = AgentPage.objects.filter(status=1).first()

    context = {
        'page': page,
        'realtors': realtors,
    }

    return render(request, 'main/agent_list.html', context)


def privacypolicy(request):
    # Get all realtors
    page = PrivacyPolicy.objects.filter(status=1).first()

    context = {
        'page': page,
    }

    return render(request, 'main/privacy_policy.html', context)



def contact(request):
    contacts = Contact.objects.filter(status=1).first()
    email_setting = EnqEmailSetting.objects.all().first()
    if email_setting and email_setting.enqmail:
        # Use enqmail if it's not empty
        enqmail = email_setting.enqmail
    # elif vendor.user:
    #     # Use the email from the associated User if available
    #     vemail = vendor.user.email
    else:
        # Fallback to a default email or handle as needed
        enqmail = "darpankario@gmail.com"
    
    if request.method == "POST":
        form = FeedbackForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data['subject']
            email = form.cleaned_data['email']
            phone = form.cleaned_data['phone']
            message = form.cleaned_data['message']
            full_name = form.cleaned_data['full_name']
            feedback = Feedback(full_name=full_name, subject=subject, email=email, phone=phone, message=message)
            feedback.save()
            msg_html = render_to_string('emails/enquiry_email.html', {'subject': subject, 'full_name': full_name, 'email': email, 'phone': phone, 'message': message})
    
            send_mail(
                subject,
                message,
                email,
                [enqmail],
                html_message=msg_html,
            )
            messages.success(request, 'Your Message has been send sucessfully!')
            return redirect('contact')
    else:
        form = FeedbackForm()
        
    
    context = {
        'contact': contacts,
        'form': form,
    }
    
    return render(request, 'main/contact.html',context)

