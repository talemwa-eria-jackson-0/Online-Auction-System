from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from . import forms
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

# Create your views here.

def home(request):
    return render(request, "core/home.html")


@login_required(login_url="login")
def dashboard(request):
    return render(request, "core/index.html")


@login_required(login_url="login")
def my_auctions(request):
    return render(request, "core/my_auctions.html")


@login_required(login_url="login")
def all_auctions(request):
    return render(request, "core/all_auctions.html")


@login_required(login_url="login")
def my_applications(request):
    return render(request, "core/my_applications.html")


@login_required(login_url="login")
def change_password(request):
    return render(request, "core/change_password.html")


@login_required(login_url="login")
def reset_password(request):
    return render(request, "core/reset_password.html")


@login_required(login_url="login")
def my_profile(request):
    return render(request, "core/my_profile.html")


# def user_register(request):
#     if request.method == "POST":
#         form = forms.RegistrationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "You have successfully created your account")
#             # proces data and create user 
#             # redirect to the login page
#             return redirect("login")
#         else:
#             # form = forms.CustomRegistrationForm()
#             messages.error(request, "Error")
#     else:
#         form = forms.RegistrationForm()

#     return render(request, "core/register.html", {
#         "form": form,
#     })


def user_login(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("dashboard")


    return render(request, "core/login.html", {
        # "page": page,
    })


def user_logout(request):
    logout(request)
    return redirect("login")


def user_register(request):
    form = forms.CustomUserCreationForm()

    if request.method == "POST":
        form = forms.UserCreationForm(request.POST)
        # registering the user to the db 
        if form.is_valid():
            user = form.save()
            # logging in the user automatically 
            login(request, user)
            return redirect("dashboard")

    return render(request, "core/register.html", {
        "form": form,
    })