from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from . import forms
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from . import models, forms
from django.utils import timezone

from django.shortcuts import get_object_or_404


from django.http import JsonResponse, HttpResponseBadRequest

from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def home(request):
    return render(request, "core/home.html")


def dashboard(request):
    all_products = models.Product.objects.all()
    ongoing_auctions = all_products.filter(end_time__gt=timezone.now())

    bids_data = {}
    for auction in ongoing_auctions:
        try:
            auction_instance = models.Auction.objects.get(product=auction)
        except ObjectDoesNotExist:
            return redirect("my_auctions")
        bids_count = models.Bid.objects.filter(auction=auction_instance).count()
        bids_data[auction.name] = bids_count
    
    bids_data_keys = list(bids_data.keys())
    bids_data_values = list(bids_data.values())

    print(bids_data_keys)
    print(bids_data_values)

    return render(request, "core/index.html", {
        "all_products": all_products,
        "ongoing_auctions": ongoing_auctions,
        "bids_data_keys": bids_data_keys,
        "bids_data_values": bids_data_values,
    })


    


def product_details(request, product_id):
    product = get_object_or_404(models.Product, pk=product_id)
    # Try to get the associated Auction object, or create one if it doesn't exist
    auction, created = models.Auction.objects.get_or_create(product=product)
    if request.method == "POST":
        bid_form = forms.BidForm(request.POST)
        if bid_form.is_valid():
            bid_amount = bid_form.cleaned_data['bid_price']
            # Ensure the bid is higher than the start price and current price
            if float(bid_amount) > float(product.start_price) and float(bid_amount) > float(auction.current_price):
                # Create a Bid model instance
                bid = models.Bid.objects.create(bidder=request.user, auction=auction, bid_price=bid_amount)
                # Update the current price in the Auction model
                auction.current_price = bid_amount
                auction.save()
                messages.success(request, "Bid submitted successfully.")
            else:
                pass
        else:
            return HttpResponseBadRequest("Invalid form data")  # Return a 400 Bad Request response for invalid form data
    bid_form = forms.BidForm()  # Create an empty form for GET requests
    highest_bid = models.Bid.objects.filter(auction=auction).order_by('-bid_price').first()
    return render(request, "core/product_details.html", {"product": product, "auction": auction, "bid_form": bid_form, "highest_bid":highest_bid})



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
    # Query for all bids made by the current user
    user_bids = models.Bid.objects.filter(bidder=request.user)

    # Extract the products associated with those bids
    products_bidded_on = [bid.auction.product for bid in user_bids]

    return render(
        request,
        "core/my_applications.html",
        {"products_bidded_on": products_bidded_on},
    )


@login_required(login_url="login")
def change_password(request):
    return render(request, "core/change_password.html")


@login_required(login_url="login")
def reset_password(request):
    return render(request, "core/reset_password.html")


@login_required(login_url="login")
def my_profile(request):
    user = models.DjangoUser.objects.get(pk=request.user.id)
    user_profile = models.UserProfile.objects.get(user=user)
    
    if request.method == 'POST':
        user_form = forms.CustomUserChangeForm(request.POST, instance=user)
        profile_form = forms.UserProfileForm(request.POST, instance=user_profile)
        
        try:
            user_profile = models.UserProfile.objects.get(user=user)
        except models.UserProfile.DoesNotExist:
            user_profile = models.UserProfile.objects.create(user=user)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            
            messages.success(request, 'Your profile is updated successfully')
            return redirect('my_profile')
    else:
        user_form = forms.CustomUserChangeForm(instance=user)
        profile_form = forms.UserProfileForm(instance=user_profile)
    
    return render(request, "core/my_profile.html", {'user_form': user_form, 'profile_form': profile_form})

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
        profile_form = forms.UserProfileForm(request.POST)
        # registering the user to the db 
        if form.is_valid():
            user = form.save()

            # Create UserProfile instance and save it
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()

            # logging in the user automatically 
            login(request, user)
            return redirect("dashboard")
    else:
        form = forms.CustomUserCreationForm()
        profile_form = forms.UserProfileForm()

    return render(request, "core/register.html", {
        "form": form,
        "profile_form": profile_form,
    })



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


@login_required(login_url="login")
def delete_product(request, product_id):
    product = get_object_or_404(models.Product, id=product_id, seller=request.user)
    
    if request.method == "POST":
        # Handle deletion here if needed
        product.delete()
        messages.success(request, "Product deleted successfully.")
        return redirect("my_auctions")

    return render(request, "core/delete_product.html", {
        "product": product,
    })

# view for showing product details
# 
def product_details(request, product_id):
    product = get_object_or_404(models.Product, pk=product_id)
    # Try to get the associated Auction object, or create one if it doesn't exist
    auction, created = models.Auction.objects.get_or_create(product=product)
    if request.method == "POST":
        bid_form = forms.BidForm(request.POST)
        if bid_form.is_valid():
            bid_amount = bid_form.cleaned_data['bid_price']
            # Ensure the bid is higher than the start price and current price
            if float(bid_amount) > float(product.start_price) and float(bid_amount) > float(auction.current_price):
                # Create a Bid model instance
                bid = models.Bid.objects.create(bidder=request.user, auction=auction, bid_price=bid_amount)
                # Update the current price in the Auction model
                auction.current_price = bid_amount
                auction.save()
                messages.success(request, "Bid submitted successfully.")
            else:
                pass
        else:
            return HttpResponseBadRequest("Invalid form data")  # Return a 400 Bad Request response for invalid form data
    bid_form = forms.BidForm()  # Create an empty form for GET requests
    highest_bid = models.Bid.objects.filter(auction=auction).order_by('-bid_price').first()
    return render(request, "core/product_details.html", {"product": product, "auction": auction, "bid_form": bid_form, "highest_bid":highest_bid})
