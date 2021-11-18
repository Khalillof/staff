from django import forms
from django.db import models
from .models import Blog,BlogPost, PostCategory
from agency.models import Office
class CategoryForm(forms.ModelForm):
    class Meta:
        model = PostCategory
        fields = ['name', 'discription']

class BlogPostForm(forms.ModelForm):
    class Meta:
        model = BlogPost
        fields = ['author','blog','category', 'title','discription','content', 'isPublic','image','pub_date']
       
        widgets = {
            'author':forms.HiddenInput(), 
           # 'blog':forms.ModelChoiceField(queryset=Blog.objects.all(),empty_label="select Blog"),
           # 'category':forms.ModelChoiceField( queryset=PostCategory.objects.all(),empty_label="select category"),
            'pub_date':forms.FileInput(attrs={'class':'form-control','type':'date','placeholder': 'publish date time'}),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['blog'].empty_label = "select Blog"
        self.fields['blog'].widget.attrs.update({'class':'form-control','placeholder': 'Chose Blog'})
        
        self.fields['category'].empty_label = "select category"
        self.fields['category'].widget.attrs.update({'class':'form-control','placeholder': 'Chose Category'})
       

        self.fields['title'].widget.attrs.update({'class':'form-control','placeholder': 'Post title','maxlength':"100"})
        self.fields['discription'].widget.attrs.update({'class':'form-control html','placeholder':"Discription", "rows":"5", "cols":"50",'maxlength':"300"})
        self.fields['content'].widget.attrs.update({'class':'form-control html','placeholder':"Post Content", "rows":"8", "cols":"50",'maxlength':"500"})
        self.fields['isPublic'].widget.attrs.update({'class':'form-control','placeholder': 'is public'})
        self.fields['image'].widget.attrs.update({'class':'form-control','placeholder': 'upload photo optional'})
        #self.fields['pub_date'].widget.attrs.update({'class':'form-control','type':'datetime','placeholder': 'publish date time'})


class BlogForm(forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['office'].empty_label = "select Office"
        self.fields['office'].widget.attrs.update({'class':'form-control','placeholder': 'offices'})
        self.fields['name'].widget.attrs.update({'class':'form-control','placeholder': 'Blog Name','maxlength':"100"})
        self.fields['discription'].widget.attrs.update({'class':'form-control html','placeholder':"Discription", "rows":"6", "cols":"50",'maxlength':"300"})
        self.fields['isPublic'].widget.attrs.update({'class':'form-control','placeholder': 'is public'})
        self.fields['image'].widget.attrs.update({'class':'form-control','placeholder': 'upload photo optional'})

    class Meta:
        model = Blog
        fields = ['author','office','name','discription','isPublic','image'] 
      
        widgets = {
            'author':forms.HiddenInput(),
            #'office':forms.ModelChoiceField(queryset=Office.objects.all() ,empty_label="select office"),
            #'name':forms.TextInput(attrs={'class':'form-control','placeholder': 'Blog Name','maxlength':"100"}),
        }
    
    



