from django.db import models
from django.contrib.auth.models import User as DjangoUser

# Create your models here.
class UserProfile(models.Model):
    user = models.OneToOneField(DjangoUser, on_delete=models.CASCADE)
    phone_number = models.CharField(max_length=10)
    address = models.TextField()

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name} from {self.address.title} ----> {self.phone_number}"


# represents the product being auctioned
class Product(models.Model):
    seller = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=255, default="New Product")
    description = models.TextField(null=True)
    start_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    end_time = models.DateTimeField(null=True)
    image = models.ImageField(upload_to='product_images/', null=True)

    def __str__(self):
        return f"{self.name}"


class Auction(models.Model):
    product = models.OneToOneField(Product, on_delete=models.CASCADE)
    current_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    winner = models.ForeignKey(DjangoUser, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.product} => {self.current_price}"


#  stores individual bids made by users on specific auctions
class Bid(models.Model):
    bidder = models.ForeignKey(DjangoUser, on_delete=models.CASCADE, default="")
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE, default="")
    bid_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)     #manually specifying the bid price
    bid_time = models.DateTimeField(auto_now_add=True, null=True)