from django.contrib.auth.models import AbstractUser
from django.db import models
from django.urls import reverse
from django import forms
from capstone.helper import images_upload_directory
# Create your models here.

class User(AbstractUser):
    email_confirmed = models.BooleanField(default=False)
    can_send_email = models.BooleanField(default=False)
    mobile = models.CharField(max_length=20, blank=True, null=True)
    image = models.FileField(blank=True, null=True,verbose_name="Photo optional",upload_to=images_upload_directory)
    imgUrl = models.CharField(max_length=100, blank=True, null=True, default="images/avatar.png")

    def full_name(self):
        return  f"{self.first_name}-{self.last_name}"

    def get_absolute_url(self):
        return reverse('user-detail', kwargs={'pk': self.pk})

    class Meta:
        ordering = ['date_joined']
    

class SiteSettings(models.Model):
    email_auth_user = models.CharField(max_length=50)
    email_auth_password = models.CharField(max_length=128, verbose_name='site_email_auth_password')
    captcha_public_key = models.CharField(max_length=200)
    captcha_secret_key = models.CharField(max_length=200)
    default = models.BooleanField(default=False)

    def __str__(self):
        return self.email_auth_user

class UserForm(forms.ModelForm):
    confirm_password=forms.CharField(widget=forms.PasswordInput(attrs={'class':'form-control',"name":'confirm_password',"id":'confirm_password','placeholder': 'Confirm password', 'maxlength':"15"}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'class':'form-control',"required":'true','placeholder': 'Username','maxlength':"40"})
        self.fields['email'].widget.attrs.update({'class':'form-control',"required":'true','placeholder': 'Your email','maxlength':"40"})
        self.fields['first_name'].widget.attrs.update({'class':'form-control',"required":'true','placeholder': 'First name','maxlength':"40"})
        self.fields['last_name'].widget.attrs.update({'class':'form-control',"required":'true','placeholder': 'First name','maxlength':"40"})
        self.fields['mobile'].widget.attrs.update({'class':'form-control','placeholder': 'mobile ', "max":"15"})
        #self.fields['password'].widget.attrs.update({'class':'form-control',"type":"password","name":'password',"id":'password','placeholder': 'Password','maxlength':"15"})
        self.fields['image'].widget.attrs.update({'class':'form-control','placeholder': 'Photo optional'})
    
    class Meta:
        model = User
        fields = ['username','email','first_name', 'last_name','mobile', 'image','password']
        
        widgets = {
            'password':forms.PasswordInput(attrs={'class':'form-control',"type":"password","name":'password',"id":'password','placeholder': 'Password','maxlength':"15"}),
        }
    
    def clean(self):
        cleaned_data = super(UserForm, self).clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError(
                "password and confirm_password does not match"
            )