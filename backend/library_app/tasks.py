from datetime import datetime

import requests
from celery import shared_task
from django.core.mail import send_mail

from .models import Book, Reservation


@shared_task
def update_book_status():
    books = Book.objects.filter(available=True)
    for book in books:
        try:
            response = requests.get(f"http://api:5000/status/{book.id}")
            data = response.json()
            book.available = data["available"]
            book.save()
        except Exception as e:
            print(f"Error updating book {book.id}: {str(e)}")


@shared_task
def send_overdue_notifications():
    overdue = Reservation.objects.filter(
        status="active", return_date__lt=datetime.now()
    )
    for reservation in overdue:
        subject = f"Overdue Reservation Notification for {reservation.book.title}"
        message = (
            f"Dear {reservation.user.username},\n\n"
            f"Your reservation for the book '{reservation.book.title}' is overdue. "
            "Please return it as soon as possible to avoid any penalties.\n\n"
            "Thank you."
        )
        recipient_list = [reservation.user.email]
        try:
            send_mail(
                subject,
                message,
                "sylwia.moscicka@outlook.com",
                recipient_list,
                fail_silently=False,
            )
            print(
                f"Notification sent to {reservation.user.email} for reservation {reservation.id}"
            )
        except Exception as e:
            print(
                f"Error sending notification for reservation {reservation.id}: {str(e)}"
            )
