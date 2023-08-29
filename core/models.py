from django.db import models

# Create your models here.

class User(models.Model):
    user_fullname = models.CharField(max_length=64)
    user_email = models.EmailField(null=True)
    user_home_town = models.CharField(max_length=64)
    user_name = models.CharField(max_length=64)

    def __str__(self):
        return f"Name: {self.user_fullname}, Home Town: {self.user_home_town}"


class Product(models.Model):
    product_name = models.CharField(max_length = 50)
    slug = models.SlugField()
    product_price = models.IntegerField()
    product_desc = models.TextField()
    product_time_posted = models.DateTimeField(auto_now_add=True)
    user_email = models.ForeignKey(User, on_delete=models.CASCADE)
    product_image = models.ImageField(null=True, blank=True)

    def __str__(self):
        return f"Name: {self.product_name}, Price: {self.product_price}"
    

class Bid(models.Model):
    pass