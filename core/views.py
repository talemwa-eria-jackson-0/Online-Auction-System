from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from . import forms
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from . import models, forms
from django.utils import timezone

from django.shortcuts import get_object_or_404

# Create your views here.

def home(request):
    return render(request, "core/home.html")


@login_required(login_url="login")
def dashboard(request):
    return render(request, "core/index.html")


# view for handling form submission for products on my_auctions.html
@login_required(login_url="login")
def my_auctions(request):
    user = request.user
    user_products = models.Product.objects.filter(seller=user)  # Getting user products

    if request.method == "POST":
        form = forms.ProductForm(request.POST, request.FILES)
        if form.is_valid():
            product = form.save(commit=False)
            product.seller = user
            product.save()
            # Redirect to a success page or refresh the current page

            # After successfully adding the product, you can display a message or redirect.
            messages.success(request, "Product added successfully.")
            return redirect("my_auctions")  # Redirect back to the same page
    else:
        form = forms.ProductForm()  # Creating a new form for rendering in the template

    return render(request, "core/my_auctions.html", {
        "form": form,
        "user_products": user_products,
    })


@login_required(login_url="login")
def all_auctions(request):
    # Retrieve all products from the database
    all_products = models.Product.objects.all()

    # Retrieve the most recent 5 products from the database
    recent_products = models.Product.objects.order_by('-id')[:5]

    # Filter products based on end_time (exclude those where end_time has passed)
    current_time = timezone.now()
    ongoing_auctions = all_products.filter(end_time__gt=current_time)
    
    return render(request, "core/all_auctions.html", {
        "all_products": all_products,
        "recent_products": recent_products,
        "ongoing_auctions": ongoing_auctions,
    })


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


# view for editing product in my_auctions 
@login_required(login_url="login")
def edit_product(request, product_id):
    product = get_object_or_404(models.Product, id=product_id, seller=request.user)

    if request.method == "POST":
        form = forms.ProductForm(request.POST, request.FILES, instance=product)
        if form.is_valid():
            form.save()
            messages.success(request, "Product updated successfully.")
            return redirect("my_auctions")

    else:
        form = forms.ProductForm(instance=product)

    return render(request, "core/edit_product.html", {
        "form": form,
        "product": product,
    })
