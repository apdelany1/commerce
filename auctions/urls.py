from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("postListing", views.postListing, name="postListing"),
    path("listing/<int:listingId>", views.listing, name="listing"),
    path("watchlist", views.watchlistPage, name="watchlistPage"),
    path("categories", views.categoriesPage, name="categoriesPage"),
    path("categories/<path:categoryName>", views.categoryPage, name="categoryPage")
]
