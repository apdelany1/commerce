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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="auctionListing", null=True)
    def __str__(self):
        return f"{self.title} with the description of {self.description} starting at {self.price} IMG: {self.photo} in category {self.category} created by {self.owner}"

class Bid(models.Model):
    startingBid = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid", null=True)

class Comment(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comments", null=True)
    auctionListing = models.ForeignKey(AuctionListing, on_delete=models.CASCADE, related_name="comments", null=True)
    content = models.TextField(null=True, blank=True)
    def __str__(self):
        return f"{self.content} said by {self.owner} on {self.auctionListing}"