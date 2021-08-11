from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render
from django.urls import reverse

from .models import Listing, User, Watchlist
from .forms import BidForm, CommentForm, ListingForm
from .Category import *
from .Constants import CATEGORY_IMAGE_URLS


def index(request):
    listings = Listing.objects.all().filter(active=True)
    return render(request, "auctions/index.html", {
        "listings": listings,
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")


@login_required
def new_listing(request):
    form = ListingForm()
    
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            listing = form.save(commit=False)
            listing.owner = request.user
            listing.save()
            return HttpResponseRedirect(reverse('index'))  
        
    return render(request, "auctions/new_listing.html", {
        'form': form
    })


@login_required
def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    watchlist = listing.watchlist.all().filter(user=request.user)
    comments = listing.comments.all().order_by("-created")
    bidform = BidForm()
    commentform = CommentForm()
    
    if request.method == "POST":
        if request.POST.get("form_type") == "bid_form":
            bidform = BidForm(request.POST, user=request.user, listing=listing)
            if bidform.is_valid():               
                bid = bidform.save(commit=False)
                bid.user = request.user
                bid.save()
                listing.bids.add(bid)
                listing.price = bid.amount
                listing.save()
                return redirect("listing", listing_id)
                    
        if request.POST.get("form_type") == "comment_form":
            commentform = CommentForm(request.POST)
            if commentform.is_valid():
                comment = commentform.save(commit=False)
                comment.user = request.user
                comment.save()
                listing.comments.add(comment)
                listing.save()
                return redirect("listing", listing_id)

        if request.POST.get("form_type") == "toggle_watchlist":
            if watchlist:
                watchlist.delete()
            else:
                watchlist = Watchlist(user=request.user, listing=listing)
                watchlist.save()
            return redirect("listing", listing_id)

        if request.POST.get("form_type") == "close_listing":
            bids = listing.bids.all().order_by("-amount")
            if bids:
                listing.owner = bids[0].user
            listing.active = False
            listing.save()
            return redirect("listing", listing_id)
    
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlist": watchlist,
        "comments": comments,
        "bidform": bidform,
        "commentform": commentform,
    })


@login_required
def watchlist(request):

    watchlist = []
    for item in request.user.watchlist.all():
        watchlist.append(item.listing)
    
    return render(request, "auctions/watchlist.html", {
        "watchlist": watchlist
    })


def categories(request):

    return render(request, "auctions/categories.html", {
        "CATEGORY_IMAGE_URLS": CATEGORY_IMAGE_URLS
    })

def category(request, category_name):

    category = Listing.objects.all().filter(category=category_name)

    return render(request, "auctions/index.html", {
        "listings": category
    })