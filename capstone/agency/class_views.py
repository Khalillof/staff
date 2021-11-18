
from django.views.generic import detail, edit
from agency.models import Advert, Application
from capstone.helper import get_exist
from django.contrib.auth.mixins import LoginRequiredMixin
from .agencyforms import ApplicationForm
from capstone.helper import get_exist

########### adverts views

class AdvertDetail(detail.DetailView):
    model = Advert  
    template_name="agency/adverts/detail.html"

    def get_object(self):
        obj = get_exist(Advert,self.kwargs["pk"])
        self.extra_context = {"title": obj.job.title}
        return obj 
    """
    def get_context_data(self, **kwargs):
        context = super(AdvertDetail, self).get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context
    """
########### applications views

class ApplicationDetail(LoginRequiredMixin, detail.DetailView):
    model = Application
    template_name="agency/application/detail.html"

    def get_object(self):
        obj = get_exist(Application,self.kwargs["pk"])
        self.extra_context= {"title": obj.advert.job.title}
        return obj 
    

class ApplicationCreate(LoginRequiredMixin, edit.CreateView):
    model = Application
    template_name="shared/create_update.html"
    form_class = ApplicationForm
    success_url = '/thank/you/' 
    extra_context = {"title":"Job Application", "html":True}
    
    def get_initial (self):   
        return {'applicant': self.request.user.id, 'advert':self.kwargs.get("advert_id")}


class ApplicationUpdate(LoginRequiredMixin, edit.UpdateView):
    model = Application 
    template_name="shared/create_update.html"
    form_class = ApplicationForm
    success_url = '/thank/you/' 
    #title = "Update Job Application"
    def get_initial (self):
        self.extra_context = {"title":"Job Application", "html":True}
        return {'applicant': self.request.user.id, 'advert':self.kwargs("advert_id")}


class ApplicationDelete(LoginRequiredMixin, edit.DeleteView):
    model = Application
    template_name="agency/application/delete.html"