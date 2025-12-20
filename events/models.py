from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum
from django.utils import timezone


# Create your models here.
class User(AbstractUser):
    is_organizer = models.BooleanField(default=False)
    is_attendee = models.BooleanField(default=False)
    interests = models.TextField(
        blank=True, help_text="Comma seperated list of event Categories"
    )


class Event(models.Model):
    CATEGORY_CHOICES = [
        ("arts", "Arts and Culture"),
        ("education", "Education and Workshops"),
        ("sports", "Sports and Fitness"),
        ("social", "Social and Networking"),
        ("food", "Food and Drink"),
        ("entertainment", "Entertainment"),
        ("technology", "Technology and Innovation"),
        ("family", "Family and Kids"),
        ("religious", "Religious and Spiritual"),
        ("holidays", "Holidays and Seasonal"),
        ("business", "Business and Corporate"),
        ("health", "Health and Wellness"),
        ("niche", "Other Niche Events"),
    ]

    STATUS_CHOICES = [
        ("active", "Active"),
        ("canceled", "Canceled"),
        ("sold_out", "Sold Out"),
        ("past", "Compeleted"),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES, default="arts")
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="events")
    location = models.CharField(max_length=200)
    date = models.DateField()
    time = models.TimeField()
    image = models.ImageField(upload_to="event-images/")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default="active")
    tickets_available = models.IntegerField(default=0)
    price = models.DecimalField(max_digits=8, decimal_places=2, default=0.0)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title}"

    def tickets_sold(self):
        return self.tickets.aggregate(total=Sum("quantity"))["total"] or 0

    def tickets_remaining(self):
        return self.tickets_available - self.tickets_sold()

    def revenue(self):
        return self.tickets_sold() * self.price

    def is_sold_out(self):
        return self.tickets_sold() >= self.tickets_available

    def is_passed(self):
        return self.date < timezone.now().date()

    def mark_as_passed(self):
        self.status = "past"
        self.save()


class Review(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="reviews")
    reviewer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="reviews")
    rating = models.PositiveSmallIntegerField(default=5)
    comment = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.event.title} - {self.rating}/5"


class Ticket(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="tickets")
    attender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="tickets")
    quantity = models.PositiveIntegerField(default=1)
    purchased_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} tickets for {self.event.title} by {self.attender.username}"
