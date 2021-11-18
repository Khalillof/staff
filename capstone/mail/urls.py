from django.urls import path

from . import views
# API Routes
app_name = 'mail'
urlpatterns = [
    path("", views.index, name="index"),
    # emailbox
    path("<str:mailbox>/<int:page>", views.MailBox_list.as_view(), name="mailbox-list"),
    path('detail/<int:pk>/', views.EmailDetail.as_view(), name='email-detail'),
    path('add/',views.EmailCreate.as_view(), name='email-add'),
    path('add/draft',views.EmailDraft.as_view(), name='email-draft'),
    path('add/draft/<int:pk>',views.EmailDraft.as_view(), name='email-draft'),   
    path('delete/<int:pk>/', views.EmailDelete.as_view(), name='email-delete'),
    # API Routes
    #path("emails", views.compose, name="compose"),
   # path("emails/<int:email_id>", views.email, name="email"),
   # path("emails/<str:mailbox>/", views.mailbox, name="mailbox"),

    path('contact/list/<int:page>', views.ContactList.as_view(), name='contact-list'),
    path('contact/detail/<int:pk>/', views.ContactDetail.as_view(), name='contact-detail'),
    path('contact/add/',views.ContactCreate.as_view(), name='contact-add'),
    #path('contact/update/<int:pk>/', views.ContactUpdate.as_view(), name='contact-update'),
    path('contact/delete/<int:pk>/', views.ContactDelete.as_view(), name='contact-delete'),
]