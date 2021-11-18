from django.db import models
from django import forms
from accounts.models import User
from django.urls import reverse
from agency.models import Office
from capstone.helper import docs_upload_directory
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
# Create your models here.

class MultiEmailField(forms.Field):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return [] 
        return value.split(',')

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        for email in value:
            validate_email(email)
        
    def clean(self, value):
        """
        Validate the given value and return its "cleaned" value as an
        appropriate Python object. Raise ValidationError for any errors.
        """
        value = self.to_python(value)
        self.validate(value)

        recipients = []

        for email in value:
            try:
                user = User.objects.get(email=email)
                recipients.append(user.id)
            except User.DoesNotExist:
               raise ValidationError(
                "error" f"User with email : {email} does not exist."
               )
               raise ValidationError("error" f"User with email : {email} does not exist.", params={'value': email},
             )
        
        value = recipients
        self.validate(value)
        #self.run_validators(value)
        return value


class Email(models.Model):
    sender = models.ForeignKey(User, on_delete=models.PROTECT, related_name="emails_sent")
    to_emails = models.CharField(max_length=255)
    subject = models.CharField(max_length=255)
    body = models.TextField(blank=True)      
    recipients = models.ManyToManyField(User, related_name="emails_received")   
    attachment = models.FileField(verbose_name="attachment",upload_to=docs_upload_directory, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    archived = models.BooleanField(default=False) 
    draft = models.BooleanField(default=False)
    trash = models.BooleanField(default=False)

    def serialize(self):
        return {
            "id": self.id,
            "sender": self.sender,
            "recipients": [user.email for user in self.recipients.all()],
            "subject": self.subject,
            "body": self.body,
            "created": self.timestamp.strftime("%A %d %B %Y %I:%M %p"),
            "read": self.read,
            "archived": self.archived,
            "draft": self.read,
            "trash": self.archived
        }

    def get_absolute_url(self):
        return reverse('email-detail', kwargs={'pk': self.pk})
    class Meta:
        ordering = ['created']
        
############ Email Form
class EmailForm(forms.ModelForm):

    class Meta:
        model = Email
        fields = ['sender','to_emails','subject','body', 'attachment','draft','trash']
    
        widgets = {
            'sender':forms.HiddenInput(),
            'to_emails':forms.EmailInput(),
            'draft':forms.HiddenInput(),
            'trash':forms.HiddenInput(),
        }
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['to_emails'].widget.attrs.update({'class':'form-control', 'autofocus': True,'placeholder': 'To: ','minlength':"3",'maxlength':"100"})
        #self.fields['sender'].widget.attrs.update({'class':'form-control','placeholder': 'your email','maxlength':"100"})
        self.fields['subject'].widget.attrs.update({'class':'form-control','autofocus': True,'placeholder': 'Subject: ','minlength':"3",'maxlength':"100"})
        self.fields['body'].widget.attrs.update({'class':'form-control html','autofocus': True,'placeholder':"Message body", 'minlength':"3"})
        #self.fields['recipients'].empty_label = "select recipients"
        #self.fields['recipients'].widget.attrs.update({'class':'form-control','placeholder': 'recipients'})
        self.fields['attachment'].widget.attrs.update({'class':'form-control','multiple': True,'placeholder': 'attachments'}),
############ Contact Model
class Contact(models.Model):
     office = models.ForeignKey(Office, on_delete=models.CASCADE) 
     name = models.CharField(max_length=100) 
     from_email = models.EmailField(max_length=70)  
     subject = models.CharField(max_length=100) 
     body = models.TextField()
     created = models.DateTimeField(auto_now=True, blank=True)
     email_confirmed = models.BooleanField(default=False)

     def get_absolute_url(self):
        return reverse('contact-detail', kwargs={'pk': self.pk})

     class Meta:
        ordering = ['created']

     def __str__(self):
        return f"Office: {self.name}"

class ContactForm(forms.ModelForm):
    
    class Meta:
        model = Contact
        fields = ['office','name', 'from_email', 'subject', 'body']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['office'].empty_label = "select Office"
        self.fields['office'].widget.attrs.update({'class':'form-control','placeholder': 'offices'})
        self.fields['name'].widget.attrs.update({'class':'form-control','placeholder': 'Name','maxlength':"100"})
        self.fields['from_email'].widget.attrs.update({'class':'form-control','placeholder': 'your email','maxlength':"100"})
        self.fields['subject'].widget.attrs.update({'class':'form-control','placeholder': 'subject','maxlength':"100"})
        self.fields['body'].widget.attrs.update({'class':'form-control','placeholder':"Discription", "rows":"6", "cols":"50",'maxlength':"500"})
        

         

        
        
