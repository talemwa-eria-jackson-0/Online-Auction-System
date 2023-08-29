from django.shortcuts import render

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
    return render(request, "core/register.html")


def login(request):
    return render(request, "core/login.html")