from django import forms
from .models import Realtor
from accounts.validators import allow_only_images_validator


class VendorForm(forms.ModelForm):
    # vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    class Meta:
        model = Realtor
        fields = ['name','phone','email']
        
    def __init__(self, *args, **kwargs):
        super(VendorForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control' 
            
            
class AgentForm(forms.ModelForm):
    # vendor_license = forms.FileField(widget=forms.FileInput(attrs={'class': 'btn btn-info'}), validators=[allow_only_images_validator])
    class Meta:
        model = Realtor
        fields = ['name',]
        
    def __init__(self, *args, **kwargs):
        super(AgentForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget.attrs['placeholder'] = 'Vendor Name'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'               

