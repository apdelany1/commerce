from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    pass

class AuctionListing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    photo = models.URLField()
    category = models.CharField(max_length=64)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owned_listings")
    active = models.BooleanField(default=True) 
    def __str__(self):
        return f"{self.title} with the description of {self.description} starting at ${self.price} IMG: {self.photo} in category {self.category} created by {self.owner}"


class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)
    auctionListing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments", null=True)
    content = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.content} said by {self.owner} on {self.auctionListing}"

class Bid(models.Model):
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="bids")
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return f"{self.user.username} place a bid of ${self.amount} on {self.listing.title}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="watchlist")
    def __str__(self):
        return f"{self.user.username} is watching {self.listing.title}"

