from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "users"

    def __str__(self):
        return self.username


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=200)
    isbn = models.CharField(max_length=13, unique=True)
    publication_year = models.IntegerField(null=True, blank=True)
    available = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "books"

    def __str__(self):
        return f"{self.title} by {self.author}"


class Reservation(models.Model):
    STATUS_CHOICES = [
        ("pending", "Oczekująca"),
        ("confirmed", "Potwierdzona"),
        ("cancelled", "Anulowana"),
        ("completed", "Zakończona"),
    ]

    book = models.ForeignKey(
        Book, on_delete=models.CASCADE, related_name="reservations"
    )
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="reservations"
    )
    reservation_date = models.DateTimeField(default=timezone.now)
    return_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "reservations"

    def __str__(self):
        return f"{self.book.title} reserved by {self.user.username}"


class SystemLog(models.Model):
    LOG_LEVELS = [
        ("INFO", "Information"),
        ("WARNING", "Warning"),
        ("ERROR", "Error"),
        ("CRITICAL", "Critical"),
    ]

    level = models.CharField(max_length=10, choices=LOG_LEVELS)
    message = models.TextField()
    source = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, related_name="logs"
    )
    trace = models.TextField(null=True, blank=True)

    class Meta:
        db_table = "system_logs"

    def __str__(self):
        return f"[{self.level}] {self.source}: {self.message[:50]}..."
