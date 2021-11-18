from django.urls import path, re_path
from django.contrib.auth import views as auth_views
from django.views.generic import TemplateView
from . import views
# API Routes
app_name = 'accounts'  
urlpatterns = [
    path("register",views.register, name="register"),
    path('add/',views.AccountCreate.as_view(), name='user-add'),
    path('profile/', TemplateView.as_view(template_name="registration/profile.html"), name="profile"),
    path('profile/update/<int:pk>/', views.AccountUpdate.as_view(), name='profile-update'),
    # rest are URLs provided by auth 

    re_path(r"^login/$", auth_views.LoginView.as_view(), name="login"),    
    #path("login", auth_views.LoginView.as_view(), name="login"),
    path("logout", auth_views.LogoutView.as_view(), name="logout"),
    path("password_change/",auth_views.PasswordChangeView.as_view(),  name='password_change'),
    path("password_change/done/",auth_views.PasswordChangeDoneView.as_view(), name='password_change_done' ),
    path("password_reset/",auth_views.PasswordResetView.as_view(), name='password_reset'),
    path("password_reset/done/",auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path("reset/<uidb64>/<token>/",auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path("reset/done/",auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
    
]
#The URLs provided by auth are:

# accounts/login/ [name='login']
# accounts/logout/ [name='logout']
# accounts/password_change/ [name='password_change']
# accounts/password_change/done/ [name='password_change_done']
# accounts/password_reset/ [name='password_reset']
# accounts/password_reset/done/ [name='password_reset_done']
# accounts/reset/<uidb64>/<token>/ [name='password_reset_confirm']
# accounts/reset/done/ [name='password_reset_complete']