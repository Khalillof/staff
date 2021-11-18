from django.shortcuts import render
from django.views.generic import detail, edit
from .models import Email, EmailForm, Contact, ContactForm
from accounts.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from capstone.helper import get_exist, AppListView, sendEmail
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def process_Emails(self, form):
    if 'to_emails' in form.cleaned_data:
        emails = form.cleaned_data['to_emails'].split(',')

        recipients = []
        for email in [email.strip() for email in emails]:
            validate_email(email.strip())
            try:
                user = User.objects.get(email=email)
                recipients.append(user.id)
            except User.DoesNotExist:
                    raise ValidationError("error" f"User with email : {email} does not exist.", params={'value': email})
             
            
            form.cleaned_data['recipients'] = recipients
    
        """If the form is valid, save the associated model."""
        
        self.object = form.save()

        # Create one email for each recipient
        for user in recipients:
            o = self.object
            email = Email(sender=o.sender,subject=o.subject,body=o.body,attachment=o.attachment)
            email.save()
            for p in recipients:
                email.recipients.add(p)
                email.save()
    return form

def index(request):   
    return render(request,"mail/mailbox.html", 
    context={
        'file_url': 'mail/inbox.html', 
         'title':'InBox', 
         'object_list':None,
         #'html':False
         })

###########mail         


class MailBox_list(AppListView):
    title = "InBox"
    template_name = "mail/inbox.html"
    model = Email
    ordering ="created"
    require_login = True
    reverse = True

    def get_isfilter(self):
        mailbox = None
        if 'mailbox' in self.kwargs:
           mailbox = self.kwargs.get("mailbox")

        if mailbox == "inbox":
          self.isfilter =  [('recipients',self.request.user.id), ('archived',False), ('draft',False), ('trash',False)]

        elif mailbox == "sent":
           self.isfilter = [('sender',self.request.user.id),('trash',False)]

        elif mailbox == "archive":
            self.isfilter = [('recipients',self.request.user.id), ('archived',True),('trash',False)]

        elif mailbox == "draft":
            self.isfilter = [('sender',self.request.user.id), ('draft',True)]

        elif mailbox == "trash":
            self.isfilter = [('recipients',self.request.user.id),('trash', True)]
        else:
            return self.isfilter
        return self.isfilter

    def get_extra_context(self):
       key = None
       if 'mailbox' in self.kwargs:
           key = self.kwargs.get("mailbox")          
       else:
           key = "inbox"
       self.title = key.capitalize()
       self.extra_context = {'file_url':f'mail/{key}.html','mailbox':key, 'title':self.title}
       
       return self.extra_context

    #isfilter = ('closed',False)

class EmailDetail(LoginRequiredMixin, detail.DetailView):
    model = Email
    title = "Email Detail"
    template_name="mail/read.html"
    """
    def get_object(self):
      
       key = None
       if 'mailbox' in self.kwargs:
           key = self.kwargs.get("mailbox")          
       else:
           key = "inbox"
       self.title = key.capitalize()
       self.extra_context = {'file_url':f'mail/{key}.html', 'title':self.title}
     
       return get_exist(Email,self.kwargs["pk"])
    """
class EmailDraft(LoginRequiredMixin,edit.CreateView):
    extra_context = {'title': "Compose email", 'html':True,} 
    model = Email
    template_name="mail/compose.html"
    form_class = EmailForm
    success_url = "/mail/sent/1"

    def form_valid(self, form):
        draft = form.cleaned_data['draft']
        trash = form.cleaned_data['trash']
        if draft is True or trash is True:            
           return super().form_valid(form)
        return super().form_valid(process_Emails(self,form))
    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        try:
            # try update approch
            self.object = self.get_object()  
            return super().post(request, *args, **kwargs)         
        except:
            # then try create approch
              self.object = None
              return super().post(request, *args, **kwargs)

class EmailCreate(LoginRequiredMixin,edit.CreateView):
    extra_context = {'title': "Compose email", 'html':True,} 
    model = Email
    template_name="mail/compose.html"
    form_class = EmailForm
    success_url = "/mail/sent/1"
    
    def get_initial (self):   
        return {'sender': self.request.user.id}

    #def form_invalid(self, form):
    #    return super().form_invalid(form)
        
    def form_valid(self, form):      
        
        return super().form_valid(process_Emails(self,form))

class EmailDelete(LoginRequiredMixin, edit.DeleteView):
    model = Email
    title ="Delete Email"
    template_name="mail/delete.html"
    success_url = "/mail/trash/1"

#################################################### contact
class ContactList(AppListView):
    model = Contact
    title = "Contact list"
    ordering ="created"
    template_name="mail/contact/list.html"
    require_login = True
    reverse = True

class ContactDetail(LoginRequiredMixin, detail.DetailView):
    model = Contact
    template_name="mail/contact/detail.html"

    def get_object(self):
        obj = get_exist(Contact,self.kwargs["pk"])
        self.extra_context= {"title": obj.name}
        return obj
    
class ContactCreate(edit.CreateView):
    extra_context = {'title': "Contact Us"} 
    model = Contact
    template_name="mail/contact/create.html"
    form_class = ContactForm
    success_url = "/thank/you"
         
class ContactDelete(LoginRequiredMixin, edit.DeleteView):
    model = Contact
    title ="Delete Contact"
    template_name="mail/contact/delete.html"
    #model.applicant = DeleteView.request.user
    success_url = "/"

###################################
### Email class

class Email_Attachement_View(edit.CreateView):
    extra_context = {'title': "Send Email"} 
    model = Email
    template_name="shared/create_update.html"
    form_class = EmailForm
    success_url = "thank/you"
    
    def form_valid(self, form):
        """If the form is valid, save the associated model."""        
        self.object = form.save()
        #return super().form_valid(form)
        return sendEmail(self.request,form)
