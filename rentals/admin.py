from django.contrib import admin, messages
from django.utils.translation import gettext_lazy as _
from .models import (
    Profile,
    Listing,
    ListingImage,
    SearchQuery,
    Booking,
    Review,
)


# Inline für Listing-Bilder
class ListingImageInline(admin.TabularInline):
    model = ListingImage
    extra = 1
    readonly_fields = ()
    fields = ("image", "alt_text")


@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display = ("id", "title", "owner", "price", "rooms", "property_type", "is_active", "views_count", "created_at")
    search_fields = ("title", "description", "location", "owner__username")
    list_filter = ("property_type", "created_at")
    readonly_fields = ("views_count", "created_at")
    inlines = (ListingImageInline,)
    ordering = ("-created_at",)
    fieldsets = (
        (None, {"fields": ("owner", "title", "description", "location")}),
        (_("Details"), {"fields": ("price", "rooms", "property_type", "is_active", "views_count")}),
    )


@admin.register(ListingImage)
class ListingImageAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "alt_text")
    search_fields = ("listing__title",)


@admin.register(SearchQuery)
class SearchQueryAdmin(admin.ModelAdmin):
    list_display = ("query", "user", "count", "created_at")
    search_fields = ("query", "user__username")
    readonly_fields = ("created_at", "count")


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "role", "phone")
    search_fields = ("user__username", "user__email", "phone")
    list_filter = ("role",)


# Admin-Aktionen für Buchungen
def make_confirmed(modeladmin, request, queryset):
    updated = queryset.update(status=Booking.STATUS_CONFIRMED)
    modeladmin.message_user(request, _("%d Buchung(en) als bestätigt markiert.") % updated, messages.SUCCESS)
make_confirmed.short_description = "Ausgewählte Buchungen bestätigen"


def make_declined(modeladmin, request, queryset):
    updated = queryset.update(status=Booking.STATUS_DECLINED)
    modeladmin.message_user(request, _("%d Buchung(en) als abgelehnt markiert.") % updated, messages.WARNING)
make_declined.short_description = "Ausgewählte Buchungen ablehnen"


def make_cancelled(modeladmin, request, queryset):
    updated = queryset.update(status=Booking.STATUS_CANCELLED)
    modeladmin.message_user(request, _("%d Buchung(en) als storniert markiert.") % updated, messages.INFO)
make_cancelled.short_description = "Ausgewählte Buchungen stornieren"


@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "start_date", "end_date", "status", "total_price", "created_at")
    search_fields = ("listing__title", "user__username")
    list_filter = ("status", "created_at")
    readonly_fields = ("created_at", "total_price")
    actions = (make_confirmed, make_declined, make_cancelled)
    date_hierarchy = "start_date"


@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ("id", "listing", "user", "rating", "created_at")
    search_fields = ("listing__title", "user__username", "comment")
    list_filter = ("rating", "created_at")
    readonly_fields = ("created_at",)