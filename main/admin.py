from django.contrib import admin
from .models import BusType, Bus, Seat, Review, SuggestionBox, Booking, Route, DepartureCity, ArrivalCity
from django.db import models
from django.db import IntegrityError

admin.site.register(BusType)
admin.site.register(DepartureCity)
admin.site.register(ArrivalCity)
# admin.site.register(Seat)



@admin.register(Seat)
class SeatAdmin(admin.ModelAdmin):
    list_display = ('bus', 'seat_number', 'is_booked')
    # def save_model(self, request, obj):
    #     if obj.seat.on_delete == models.CASCADE:
    #         messages.warning(request, 'Reletated seat will be deleted')
    #         super().delete_model(request, obj)


@admin.register(Bus)
class BusAdmin(admin.ModelAdmin):
    list_display = ('name', 'bus_type', 'max_seats', 'bus_number', 'has_air_conditioning', 'has_wifi')
    list_filter = ('bus_type', 'has_air_conditioning', 'has_wifi', 'has_tv', 'leather_seats')
    search_fields = ('name', 'bus_number')
    prepopulated_fields = {'slug': ('name',)}  # Auto-populate slug from name

@admin.register(Route)
class RouteAdmin(admin.ModelAdmin):
    list_display = ('departure_city', 'arrival_city', 'departure_time', 'arrival_time', 'price')
    list_filter = ('departure_city', 'arrival_city', 'departure_time')
    search_fields = ('departure_city__name', 'arrival_city__name')
    
@admin.register(Booking)
class BookingAdmin(admin.ModelAdmin):
    list_display = ('user', 'route', 'seat', 'booking_date', 'receipt_number', 'payment_status')
    list_filter = ('route__departure_city', 'route__arrival_city', 'payment_status')
    search_fields = ('user__username', 'receipt_number')

@admin.register(SuggestionBox)
class SuggestionBoxAdmin(admin.ModelAdmin):
    list_display = ('full_name', 'email', 'message', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('full_name', 'email')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'rating', 'created_at', 'is_approved')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('user__username', 'title')
    actions = ['approve_reviews']

    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Approve selected reviews"