
from agency.models import  Advert, Application
from capstone.helper import get_exist, AppListView
from .models import JobCategory, Advert
#import re


class Advert_listView(AppListView):
    title = " Avaliable jobs"
    template_name = "agency/adverts/index.html"
    model = Advert
    ordering ="created"
    extra_context = {'categories': JobCategory.objects.all().order_by("created")}
    isfilter = [('closed',False)]
    
class JobCategory_listView(AppListView):
    model = Advert
    ordering ="created"
    template_name="agency/adverts/index.html"
    extra_context = {'categories': JobCategory.objects.all().order_by("created")}
    #isfilter = [('closed',False)]
    #reverse = True

    def get_title(self):
        cat_id = self.kwargs["category_id"]
        data_num = Advert.objects.filter(category=cat_id).count()
        cat = get_exist(JobCategory, cat_id)
        self.title = "Avaliable jobs for categoy : " + cat.name + ", " +  str(data_num) + " found"
        return self.title

    def get_queryset(self):
        return Advert.objects.filter(category=self.kwargs["category_id"])


class Application_viewList(AppListView):
    model = Application
    #paginate_by = 10  
    template_name="agency/application/list.html"
    ordering ="created"
    title = "Job Applications"
    require_login = True

