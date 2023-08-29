from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("my_auctions/", views.my_auctions, name="my_auctions"),
    path("all_auctions/", views.all_auctions, name="all_auctions"),
    path("my_applications/", views.my_applications, name="my_applications"),
    path("reset_password/", views.reset_password, name="reset_password"),
    path("change_password/", views.change_password, name="change_password"),
    path("my_profile/", views.my_profile, name="my_profile"),
]