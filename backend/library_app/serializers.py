from rest_framework import serializers

from .models import Book, Reservation, SystemLog


class BookSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = ["id", "title", "author", "isbn", "publication_year", "available"]


class ReservationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Reservation
        fields = ["id", "book", "user", "reservation_date", "return_date", "status"]


class SystemLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = SystemLog
        fields = ["id", "timestamp", "action", "details", "user"]
