from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import User , UserForm
from django.views.generic import  edit

# Create your views here.

class AccountCreate(edit.CreateView):
    extra_context = {'title':"Create new account"}
    model = User
    template_name="shared/create_update.html"
    form_class = UserForm
    success_url = '/accounts/login/'

    def form_valid(self, form):
        """If the form is valid, save the associated model."""
        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]
        form.save()
        u = User.objects.get(username=username)
        u.set_password(password)
        self.object = u.save()   

        return HttpResponseRedirect('/accounts/login/')

class AccountUpdate(edit.UpdateView):
    extra_context = {'title':"Update your details"}
    model = User
    template_name="shared/create_update.html"
    form_class = UserForm
    success_url = '/accounts/login/'
   
    def form_valid(self, form):
        """If the form is valid, save the associated model."""

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        form.save()

        u = User.objects.get(username=username)
        u.set_password(password)
        self.object = u.save()   

        return HttpResponseRedirect('/accounts/login/')

def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "accounts/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "accounts/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "registration/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "registration/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect("/")
    else:
        return render(request, "registration/register.html")
