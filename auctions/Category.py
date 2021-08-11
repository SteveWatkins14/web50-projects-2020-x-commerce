from django.db import models

class Category(models.TextChoices):
    BEAUTY = "Beauty"
    BOOKS = "Books"
    CDS = "CDs"
    CLOTHING = "Clothing"
    COMPUTERS = "Computers"
    HOME_AND_KITCHEN = "Home & Kitchen"
    SHOES_AND_BAGS = "Shoes & Bags"
    TOYS_AND_GAMES = "Toys & Games"
