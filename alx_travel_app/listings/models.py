""" Define database tables"""
from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    """Custome user representing a system user who can book or write review"""
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    phone = models.CharField(max_length=20, blank=True)
    role = models.CharField(max_length=10, choices=[('guest', 'Guest'), ('host', 'Host')])
    email = models.EmailField(unique=True)
    
    REQUIRED_FIELDS = ['first_name', 'last_name']
    USERNAME_FIELD = "username"
    
    def __str__(self):
        return f"{self.username} ({self.email})"


class Listing(models.Model):
    """Model representing places that users can book"""
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price_per_night = models.DecimalField(max_digits=8, decimal_places=2)
    host = models.ForeignKey(User, on_delete=models.CASCADE, related_name="hosted_listings")
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        """Method displays name of the listing when shown in admin or shell"""
        return f"{self.title} - {self.location}"


class Booking(models.Model):
    """Model represents booking list based on the user(user's reservation)"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bookings")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bookings")
    check_in_date = models.DateField()
    check_out_date = models.DateField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Booking by {self.user} for {self.listing}"

    
class Review(models.Model):
    """Review model representing feedback given by user based on a place"""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField()
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("user", "listing")

    def __str__(self):
        return f"Review by {self.user.username} on {self.listing.title}"


class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='payments')
    booking_reference = models.CharField(max_length=100, unique=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    transaction_id = models.CharField(max_length=100, blank=True, null=True)
    status = models.CharField(max_length=20, default='Pending')  # Pending, Completed, Failed
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.booking_reference} - {self.status}"