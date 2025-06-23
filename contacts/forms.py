from django import forms
from accounts.models import User, UserProfile
# from accounts.validators import allow_only_images_validator
from contacts.models import  ListingEnquiry,Feedback


class ListingEnquiryForm(forms.ModelForm):
    class Meta:
        model= ListingEnquiry
        fields=[
            'listing_name','listing_url','full_name','email','phone_no','city','requirement','user_id'
        ]
    # country = forms.ModelChoiceField(queryset=Country.objects.all(), empty_label="Select Country")    
        # widgets = {
        # 'message':forms.Textarea(attrs={'rows': 3, 'cols': 30})
        # }
    def __init__(self, *args, **kwargs):
        super(ListingEnquiryForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['placeholder'] = 'Your Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['phone_no'].widget.attrs['placeholder'] = 'Phone No.'
        self.fields['city'].widget.attrs['placeholder'] = 'Your City Name'
        self.fields['requirement'].widget.attrs['placeholder'] = 'Type Your Message'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'
            

class FeedbackForm(forms.ModelForm):
    class Meta:
        model=Feedback
        fields=[
            'full_name','subject','email','phone','message'
        ]
        # widgets = {
        # 'message':forms.Textarea(attrs={'rows': 3, 'cols': 30})
        # }
    def __init__(self, *args, **kwargs):
        super(FeedbackForm, self).__init__(*args, **kwargs)
        self.fields['full_name'].widget.attrs['placeholder'] = 'Your Name'
        self.fields['subject'].widget.attrs['placeholder'] = 'Subject'
        self.fields['email'].widget.attrs['placeholder'] = 'Email'
        self.fields['phone'].widget.attrs['placeholder'] = 'Phone No.'
        self.fields['message'].widget.attrs['placeholder'] = 'Type Your Message'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'            