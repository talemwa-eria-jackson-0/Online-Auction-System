from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("dashboard/", views.dashboard, name="dashboard"),
    path("my_auctions/", views.my_auctions, name="my_auctions"),
    path("all_auctions/", views.all_auctions, name="all_auctions"),
    path("my_applications/", views.my_applications, name="my_applications"),
    path("reset_password/", views.reset_password, name="reset_password"),
    path("change_password/", views.change_password, name="change_password"),
    path("my_profile/", views.my_profile, name="my_profile"),
    path("register/", views.user_register, name="register"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.user_logout, name="logout"),
    # path("add_product/", views.add_product, name="add_product"),
    path("edit_product/<int:product_id>/", views.edit_product, name="edit_product"),
    path("delete_product/<int:product_id>/", views.delete_product, name="delete_product"),
    path('product_details/<int:product_id>/', views.product_details, name='product_details'),

]