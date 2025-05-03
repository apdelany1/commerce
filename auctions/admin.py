from django.contrib import admin
from .models import AuctionListing, Bid, Comment, User

# Register your models here.

class AuctionListingAdmin(admin.ModelAdmin):
    list_display = ("__str__",)

class BidAdmin(admin.ModelAdmin):
    list_display = ("__str__",)

class CommentAdmin(admin.ModelAdmin):
    list_display = ("__str__",)

admin.site.register(AuctionListing, AuctionListingAdmin)
admin.site.register(Bid, BidAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(User)
