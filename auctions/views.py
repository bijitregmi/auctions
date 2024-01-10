from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib import messages
from .models import User, Listing, Bid, Comment
from .forms import ListingFrom, BidForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.db.models import Max
from django.contrib import messages


def index(request):
    listings = Listing.objects.all()
    return render(request, "auctions/index.html", {
        'listings': listings
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
            return HttpResponseRedirect(reverse("auctions:index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("auctions:index"))


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
        return HttpResponseRedirect(reverse("auctions:index"))
    else:
        return render(request, "auctions/register.html")

@login_required(login_url="auctions:login")
def create(request):
    new_listing_form = ListingFrom()
    if request.method == "POST":
        new_listing_form = ListingFrom(request.POST)

        # Check form validity
        if new_listing_form.is_valid():
            new_listing = new_listing_form.save(commit=False)

            # Set static image if no image
            if not new_listing.image:
                new_listing.image = "/static/auctions/noimage.jpg"

            # Set listing creator
            new_listing.creator = request.user

            # Save listing
            new_listing.save()
            return HttpResponseRedirect(reverse('auctions:index'))
        
        # Invalid form
        else:
            return render(request, "auctions/create.html", {
            "form": new_listing_form,
            "message": "Invalid data"
        })

    return render(request, "auctions/create.html", {
        "form": new_listing_form
    })

def listing(request, pk):
    listing = Listing.objects.get(pk=pk)
    bid_form = BidForm()
    comment_form = CommentForm()
    comments = Comment.objects.filter(listing=listing)
    return render(request, "auctions/listing.html", {
        "listing": listing,
        "watchlist": listing.watchlist.all(),
        "bid_form": bid_form,
        "comment_form": comment_form,
        "comments": comments
    })

@login_required(login_url="auctions:login")
def watchlist(request, pk):
    listing = Listing.objects.get(pk=pk)

    # Add or remove user from listing watchlist
    if request.method == "POST":
        if 'add' in request.POST:
            listing.watchlist.add(User.objects.get(pk=request.user.id))
            return HttpResponseRedirect(reverse('auctions:listing', kwargs={'pk': listing.id})) 
        else:
            listing.watchlist.remove(User.objects.get(pk=request.user.id))
            return HttpResponseRedirect(reverse('auctions:listing', kwargs={'pk': listing.id}))
    
    return HttpResponseRedirect(reverse('auctions:listing', kwargs={'pk': listing.id}))

@login_required(login_url="auctions:login")
def bid(request, pk):

    # Get bid value
    if request.method == "POST":
        bid_form = BidForm(request.POST)

        # Check validity
        if bid_form.is_valid():
            new_bid = bid_form.save(commit=False)
            listing = Listing.objects.get(pk=pk)

            # Get highest bid
            max_bid = Bid.objects.filter(item=listing).aggregate(Max("amount"))

             # Set max bid value
            if not max_bid["amount__max"]:
                max_bid["amount__max"] = listing.price

            # Check if bid is high enough
            if new_bid.amount <= listing.price or new_bid.amount <= max_bid["amount__max"]:
                messages.error(request, "Bid too small")
                HttpResponseRedirect(reverse("auctions:listing", kwargs={'pk': listing.id}))
            
            # Set values for new bid
            else:
                new_bid.bidder = request.user
                new_bid.item = listing
                listing.price = new_bid.amount
                new_bid.save()
                listing.save()

    return HttpResponseRedirect(reverse('auctions:listing', kwargs={'pk': listing.id}))

@login_required(login_url="auctions:login")
def close(request, pk):

    # Close listing
    if request.method == "POST":
        listing = Listing.objects.get(pk=pk)
        listing.active = False

        # Get latest bid
        winner = Bid.objects.filter(item=listing).latest("amount")

        # If no bids
        if not winner:
            winner = listing.creator

        listing.winner = winner.bidder
        listing.save()
    return HttpResponseRedirect(reverse('auctions:listing', kwargs={'pk': listing.id}))

@login_required(login_url="auctions:login")
def comment(request, pk):
    
    # Get comment
    if request.method == "POST":
        comment_form = CommentForm(request.POST)
        
        # Save new comment
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.by = request.user
            new_comment.listing = Listing.objects.get(pk=pk)
            new_comment.save()

    return HttpResponseRedirect(reverse("auctions:listing", kwargs={'pk': pk}))

@login_required(login_url="auctions:login")
def watchlist_view(request):
    watchlist_items = request.user.on_watchlist.all()
    return render(request, "auctions/index.html", {
        'listings': watchlist_items
    })

@login_required(login_url="auctions:login")
def categories(request):
    categories = Listing.CATEGORIES
    return render(request, "auctions/categories.html", {
        "categories": categories
    })

@login_required(login_url="auctions:login")
def category_view(request, category):
    listings = Listing.objects.filter(category=category)
    return render(request, "auctions/index.html", {
        "listings": listings
    })