from django import forms
from .models import User, UserProfile
from .validators import allow_only_images_validator


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput())
    confirm_password = forms.CharField(widget=forms.PasswordInput())
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email','phone_number','password']

    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password != confirm_password:
            raise forms.ValidationError(
                "Password does not match!"
            )
    
    
    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        self.fields['first_name'].widget.attrs['placeholder'] = 'First Name'
        self.fields['last_name'].widget.attrs['placeholder'] = 'Last Name'
        self.fields['email'].widget.attrs['placeholder'] = 'Email Address'
        self.fields['phone_number'].widget.attrs['placeholder'] = 'Mobile Number'
        # self.fields['username'].widget.attrs['placeholder'] = 'Username'
        self.fields['password'].widget.attrs['placeholder'] = 'Password'
        self.fields['confirm_password'].widget.attrs['placeholder'] = 'Confirm password'
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control unicase-form-control text-input'        


class UserProfileForm(forms.ModelForm):
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Start typing...', 'required': 'required'}))
    profile_picture = forms.FileField(widget=forms.FileInput(attrs={'type': 'file', 'class': 'upload'}), validators=[allow_only_images_validator])
    
    class Meta:
        model = UserProfile
        fields = ['profile_picture', 'bio', 'address', 'country', 'state', 'city', 'pin_code']
        
        # widgets = {
        # 'email': forms.TextInput(attrs={'type': 'email','class': 'form-control', 'placeholder': 'Email','readonly':'readonly',}),
        # } 
        
        
    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'


class UserInfoForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name','last_name','phone_number','email','username']
        widgets = {
        'email': forms.TextInput(attrs={'type': 'email','class': 'form-control', 'placeholder': 'Email','readonly':'readonly',}),
        'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'username', 'readonly':'readonly',}),
        } 
        
    def __init__(self, *args, **kwargs):
        super(UserInfoForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].widget.attrs['class'] = 'form-control'    