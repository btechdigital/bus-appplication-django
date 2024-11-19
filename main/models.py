from django.db import models
from django.conf import settings
from django.utils.text import slugify
from django.contrib.auth.models import User

class BusType(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name

class Bus(models.Model):
    bus_type = models.ForeignKey(BusType, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)  # Ensure the slug is unique
    max_seats = models.IntegerField()
    bus_number = models.CharField(max_length=100, unique=True)
    image = models.ImageField(upload_to='bus_images/', null=True, blank=True)

    # Facilities
    has_air_conditioning = models.BooleanField(default=False)
    has_wifi = models.BooleanField(default=False)
    has_tv = models.BooleanField(default=False)
    leather_seats = models.BooleanField(default=False)
    has_charging_ports = models.BooleanField(default=False)
    has_reclining_seats = models.BooleanField(default=False)
    catering_facilities = models.BooleanField(default=False)
    has_public_bathroom = models.BooleanField(default=False)  # Updated naming for consistency
    content = models.TextField(blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            counter = 1
            while Bus.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.name} => {self.bus_type} ' 
        

class Seat(models.Model):
    bus = models.ForeignKey(Bus, on_delete=models.CASCADE, null=True, related_name='seats')
    seat_number = models.IntegerField()
    is_booked = models.BooleanField(default=False)

    def __str__(self):
        return f'Seat {self.seat_number} on {self.bus.name if self.bus else "No Bus"}'

    def save(self, *args, **kwargs):
        if self.seat_number > self.bus.max_seats:
            raise ValueError("Seat number exceeds maximum seats for this bus")
        super().save(*args, **kwargs)




class DepartureCity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class ArrivalCity(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name



class Route(models.Model):
    departure_city = models.ForeignKey(DepartureCity, on_delete=models.CASCADE)
    arrival_city = models.ForeignKey(ArrivalCity, on_delete=models.CASCADE)
    departure_time = models.TimeField()
    arrival_time = models.TimeField()
    image = models.ImageField(upload_to='route_images/', null=True, blank=True)
    content = models.TextField(blank=True, null=True)
    
    # Price field added to the Route model
    price = models.DecimalField(max_digits=10, decimal_places=2)

    # Relationship to the Bus model
    buses = models.ManyToManyField('Bus', related_name='routes')

    # New boolean field
    mark_all_as_available = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        if self.mark_all_as_available:
            for bus in self.buses.all():
                bus.seat_set.update(is_booked=False)
            self.mark_all_as_available = False  # Reset after use
            super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.departure_city} - {self.arrival_city}"


class Booking(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="bookings")
    route = models.ForeignKey(Route, on_delete=models.SET_DEFAULT, default="No Route", )
    seat = models.ForeignKey(Seat, on_delete=models.SET_DEFAULT, default="No Seats")
    booking_date = models.DateTimeField(auto_now_add=True)
    receipt_number = models.CharField(max_length=100, unique=True, blank=True)
    payment_status = models.CharField(max_length=50, default='pending')  # New field to track payment status

    def __str__(self):
        return f"{self.user.username} - {self.seat.bus.name}"

    def save(self, *args, **kwargs):
        if not self.receipt_number:
            self.receipt_number = self.generate_receipt_number()
        super().save(*args, **kwargs)

    def generate_receipt_number(self):
        import uuid
        return str(uuid.uuid4())[:8]



class SuggestionBox(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100, null=True, blank=True)  # Optional email field for follow-up
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set the field to now every time the object is saved

    def __str__(self):
        return self.full_name

class Review(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    message = models.TextField()
    rating = models.PositiveSmallIntegerField(null=True, blank=True)  # Optional rating field (1-5 stars)
    created_at = models.DateTimeField(auto_now_add=True)  # Automatically set the field to now when the object is created
    updated_at = models.DateTimeField(auto_now=True)  # Automatically set the field to now every time the object is saved
    is_approved = models.BooleanField(default=False)  # A flag to mark reviews as approved by admin

    def __str__(self):
        return self.title
