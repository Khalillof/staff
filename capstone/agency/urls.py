from django.urls import path
from capstone.helper import template_page
from . import views
from . import class_views
# API Routes
app_name = 'agency'   
urlpatterns = [
    path("", template_page.as_view(template_name="agency/home/index.html"),kwargs={'title': "Home Page"},name="index"),  
    path('about/', template_page.as_view(title="About Page",template_name="agency/home/about.html"),kwargs={'title': "About Page"}, name="about"),
    path('privacy', template_page.as_view(template_name="agency/home/privacy.html"),kwargs={'title': "Privacy Policy"}, name="privacy"),
    # adverts
    path("adverts/<int:page>", views.Advert_listView.as_view(), name="adverts"),
    path('adverts/<int:category_id>/<int:page>', views.JobCategory_listView.as_view(), name='category-list'),
    path('advert/detail/<int:pk>/', class_views.AdvertDetail.as_view(), name='advert-detail'),  
    
    # applications
    path('applications/<int:page>', views.Application_viewList.as_view(), name='applications'),
    path('application/detail/<int:pk>/', class_views.ApplicationDetail.as_view(), name='application-detail'),
    path('application/add/<int:advert_id>/',class_views.ApplicationCreate.as_view(), name='application-add'),
    path('application/update/<int:pk>/', class_views.ApplicationUpdate.as_view(), name='application-update'),
    path('application/delete/<int:pk>/', class_views.ApplicationDelete.as_view(), name='application-delete'),
    path('thank/you/', template_page.as_view(template_name="shared/thanks.html"),kwargs={'title': "Thank you"}, name="thank-you"),
]

# url without namespacing 
# <li><a href="{% url 'detail' question.id %}">{{ question.question_text }}</a></li>

# example url with namesapacing
# <li><a href="{% url 'agency:detail' question.id %}">{{ question.question_text }}</a></li>
# <form action="{% url 'polls:vote' question.id %}" method="post">

# reverse url with namespacing
# from django.urls import reverse
# >>> response = client.get(reverse('polls:index'))

# add {% load static %} then followed by 
# <link rel="stylesheet" type="text/css" href="{% static 'polls/style.css' %}">