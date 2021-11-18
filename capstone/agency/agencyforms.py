from django import forms
from agency.models import JobCategory,Address, Application

def Exist(model, qs):
    try:
        item = model.objects.get(id=qs)
    except model.DoesNotExist:
        item = None
    return item

class CategoryForm(forms.ModelForm):
    class Meta:
        model = JobCategory
        fields = ['name', 'discription']

class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = ['first_line', 'street_name','city','country', 'zip_code', 'address_type']
        
    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control'


class ApplicationForm(forms.ModelForm):

    class Meta:
        model = Application
        fields = ['applicant','advert','cover_letter','cv',]        
        widgets = {
            'applicant':forms.HiddenInput(attrs={'name':'applicant'}),
            'advert':forms.HiddenInput(attrs={'name': 'advert'}),
            'cover_letter':forms.Textarea(attrs={'class':'form-control html','placeholder': 'Cover letter'}),
            'cv':forms.FileInput(attrs={'class':'form-control','placeholder': 'upload CV'}),
        }

    class Media:

        js = (
             'agency/plugins/jquery/jquery.min.js', # jquery
            'agency/plugins/summernote/summernote-bs4.min.js',   
            'agency/js/html.js', 
        )
        css = {
           'all': ('agency/plugins/summernote/summernote-bs4.min.css',)
        }
    
