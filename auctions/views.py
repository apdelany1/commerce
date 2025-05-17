from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import AuctionListing, Bid, Watchlist, Comment, User

def index(request):
    listing = AuctionListing.objects.all()
    listingData = []

    for listing in listing:
        highestBid = Bid.objects.filter(listing=listing).order_by('-amount').first()
        listingData.append({
            "listing": listing,
            "highestBid": highestBid
        })

    return render(request, "auctions/index.html", {
        "listing":listing,
        "listingData": listingData
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
def postListing(request):
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        startingBid = request.POST["startingBid"]
        photoURL = request.POST["photoURL"]
        category = request.POST["category"]

        listing = AuctionListing(
            title=title,
            description=description,
            price=startingBid,
            photo=photoURL,
            category=category,
            owner=request.user
        )

        listing.save()
        return HttpResponseRedirect(reverse("index"))

    else:
        return render(request, "auctions/postListing.html")


@login_required
def listing(request, listingId):
    listing = get_object_or_404(AuctionListing, id=listingId)
    owner = listing.owner
    watching = Watchlist.objects.filter(user=request.user, listing=listing).exists()
    noBid = Bid.objects.filter(listing=listing).exists()
    errorMessage = ""
    highestBidder = Bid.objects.filter(listing=listing).order_by('-amount').first()
    allComments = Comment.objects.filter(auctionListing=listing) 


    if request.method == "POST":
        if "addWatchlist" in request.POST:
            Watchlist.objects.create(user=request.user, listing=listing)
            return redirect("listing", listingId=listingId)
        elif "removeWatchList" in request.POST:
            Watchlist.objects.filter(user=request.user, listing=listing).delete()
            return redirect("listing", listingId=listingId)

        elif "addBid" in request.POST:
            try:
                bidAmount = float(request.POST["bid"])
                hasBid = Bid.objects.filter(listing=listing).exists()

                if hasBid == False:
                    if bidAmount > listing.price:
                        Bid.objects.create(
                            listing=listing,
                            user=request.user,
                            amount=bidAmount
                        )
                        return redirect("listing", listingId=listingId)
                    else:
                        errorMessage = "Your bid must be higher plz."
                else:
                    highestBid = Bid.objects.filter(listing=listing).order_by('-amount').first()
                    if bidAmount > highestBid.amount:
                        existingBid = Bid.objects.filter(user=request.user, listing=listing).first()
                        existingBid.amount = bidAmount
                        existingBid.save()
                        return redirect("listing", listingId=listingId)
                    else:
                        errorMessage = "Your bid must be higher plz."
            except ValueError:
                errorMessage = "Please enter a valid bid dude"
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "watching": watching,
                "bid": noBid,
                "error": errorMessage,
                "owner": owner,
                "highestBidder": highestBidder
            })

        elif "closeListing" in request.POST:
            activeStatus = AuctionListing.objects.filter(title=listing.title).first()
            activeStatus.active = False
            activeStatus.save()
            return redirect("listing", listingId=listingId)

        elif "addComment" in request.POST:
            post = request.POST["comment"]

            comment = Comment(
                owner = request.user,
                auctionListing = listing,
                content = post
            )
            comment.save() 
            return redirect("listing", listingId=listingId)


    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "watching": watching,
            "bid": noBid,
            "error": errorMessage,
            "owner": owner,
            "highestBidder": highestBidder,
            "allComments": allComments
        })

@login_required
def watchlistPage(request):
    watchList = Watchlist.objects.filter(user=request.user)
    if request.method == "GET":
        return render(request, "auctions/watchlist.html", {
            "watchList": watchList,
        })


def categoriesPage(request):
    if request.method == "GET":
        categories = (
            "electronics",
            "home+kitchen",
            "clothing",
            "food",
            "sporting"
        )

        return render(request, "auctions/categories.html", {
            "categories": categories
        })
    

def categoryPage(request, categoryName):
    categoryItems = AuctionListing.objects.filter(category=categoryName, active=True)

    if request.method == "GET":
        return render(request, "auctions/category.html", {
            "categoryItems": categoryItems,
            "categoryName": categoryName
        })
