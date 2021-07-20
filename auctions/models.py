from django.contrib.auth.models import AbstractUser
from django.db import models
from enum import Enum
from django.db.models.base import Model
from django.db.models.deletion import CASCADE, SET_NULL
from enumfields import EnumField

class Category(Enum):
    NORMAL = "NORMAL"
    FIGHT = 'FIGHT'
    FLYING = 'FLYING'


class User(AbstractUser):
    def __str__(self):
        return f"Name: {self.username}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    discription = models.TextField(max_length=500)
    image_url = models.URLField(blank=True)
    category = EnumField(Category, max_length=6, null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, to_field="id", null=True, on_delete=models.SET_NULL, related_name="listings")
    starting_bid = models.IntegerField()
    active = models.BooleanField(default=True)
    winning_bid = models.ForeignKey("Bid", to_field="id", on_delete=models.CASCADE, related_name="item", null=True, blank=True)

    def __str__(self):
        return f"Title: {self.title}, Starting Bid: {self.starting_bid}"

class Bid(models.Model):
    bidder = models.ForeignKey(User, to_field="id", null=True, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, to_field="id", on_delete=models.CASCADE, related_name="item")
    created = models.DateTimeField(auto_now_add=True)
    bid = models.IntegerField()

    def __str__(self):
        return f"Item: {self.listing}, Bid: {self.bid}, Amount: {self.bid}"

class Comment(models.Model):
    commenter = models.ForeignKey(User, to_field="id", on_delete=models.CASCADE, related_name="comments")
    listing = models.ForeignKey(Listing, to_field="id", on_delete=models.CASCADE, related_name="user_comments")
    created = models.DateTimeField(auto_now_add=True)
    comment = models.TextField(max_length=500)

    def __str__(self):
        return f"Commenter: {self.commenter}, Date: {self.created}"

class Watchlist(models.Model):
    watcher = models.ForeignKey(User, to_field="id", on_delete=models.CASCADE, related_name="watchlist")
    listing = models.ForeignKey(Listing, to_field="id", on_delete=models.CASCADE, related_name="watchlist")

    def __str__(self):
        return f"Watcher: {self.watcher.username}, Listing: {self.listing.title}"