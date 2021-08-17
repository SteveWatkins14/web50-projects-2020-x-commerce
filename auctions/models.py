from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models.deletion import CASCADE
from .Category import *
from django.core.validators import MinValueValidator

class User(AbstractUser):
    def __str__(self):
        return f"User: {self.username}"

class Listing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listings")
    title = models.CharField(max_length=64)
    discription = models.TextField(max_length=500)
    price = models.PositiveIntegerField(validators=[MinValueValidator(1)])
    category = models.CharField(max_length=14, choices=Category.choices, null=True, blank=True)
    image_url = models.URLField(blank=True)
    active = models.BooleanField(default=True)

    def __str__(self):
        return f"Title: {self.title}, Price: {self.price}"

class Bid(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidders")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    amount = models.PositiveIntegerField()

    def __str__(self):
        return f"Bidder: {self.user.username}, Listing: {self.listing.title},  Amount: {self.amount}"

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="commenter")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment")
    text = models.TextField(max_length=500)
    created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"Commenter: {self.user}, Created: {self.created}"

class Watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"Watcher: {self.user.username}, Listing: {self.listing.title}"