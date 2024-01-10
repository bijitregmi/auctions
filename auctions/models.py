from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    CATEGORIES = [
        ('BASIC', 'Basic'),
        ('CLOTHING', 'Clothing'),
        ('ELECTRONICS', 'Electronics'),
        ('FURNITURE', 'Furniture'),
        ('SPORTING GOODS', 'Sporting goods'),
        ('TOILETRIES', 'Toiletries'),
        ('TOYS', 'Toys')
    ]

    name = models.CharField(max_length=64)
    description = models.TextField(max_length=200, blank=True, null=True)
    image = models.CharField(max_length=200, blank=True, null=True)
    category = models.CharField(max_length=32, choices=CATEGORIES, default='BASIC')
    active = models.BooleanField(default=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, related_name="creator", blank=True, null=True)
    watchlist = models.ManyToManyField(User, blank=True, related_name="on_watchlist")
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="listing_winner")



    def __str__(self):
        return f"{self.name}"

class Bid(models.Model):
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bid", blank=True, null=True)
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder", blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Bid ${self.amount} on {self.item} by {self.bidder}"

class Comment(models.Model):
    comment = models.TextField(max_length=200, blank=True, null=True)
    by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment", blank=True, null=True)
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment", blank=True, null=True)

    def __str__(self):
        return f"{self.comment} by {self.by} on {self.listing}"