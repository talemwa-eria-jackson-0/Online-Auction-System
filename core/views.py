from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from . import forms
from django.contrib import messages

# Create your views here.

def home(request):
    return render(request, "core/home.html")


def dashboard(request):
    return render(request, "core/index.html")


def my_auctions(request):
    return render(request, "core/my_auctions.html")


def all_auctions(request):
    return render(request, "core/all_auctions.html")


def my_applications(request):
    return render(request, "core/my_applications.html")


def change_password(request):
    return render(request, "core/change_password.html")


def reset_password(request):
    return render(request, "core/reset_password.html")


def my_profile(request):
    return render(request, "core/my_profile.html")


def register(request):
    if request.method == "POST":
        form = forms.RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "You have successfully created your account")
            # proces data and create user 
            # redirect to the login page
            return redirect("login")
        else:
            # form = forms.CustomRegistrationForm()
            messages.error(request, "Error")
    else:
        form = forms.RegistrationForm()

    return render(request, "core/register.html", {
        "form": form,
    })


def login(request):
    return render(request, "core/login.html")