# -*- coding: utf-8 -*-
import pytest
from django.test import TestCase
from django.urls import reverse
from library_app.models import Book, Reservation, User
from library_app.serializers import BookSerializer, ReservationSerializer
from rest_framework import status
from rest_framework.test import APIClient


class BookViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            publication_year=2024,
            available=True,
        )

        self.book_url = reverse("library_app:v1:book-detail", args=[self.book.id])
        self.book_status_url = reverse(
            "library_app:v1:book-status", args=[self.book.id]
        )
        self.books_url = reverse("library_app:v1:book-list")

    def test_get_book_list(self):
        response = self.client.get(self.books_url)
        books = Book.objects.all()
        serializer = BookSerializer(books, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_get_book_detail(self):
        response = self.client.get(self.book_url)
        serializer = BookSerializer(self.book)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_book(self):
        data = {
            "title": "New Book",
            "author": "New Author",
            "isbn": "9876543210123",
            "publication_year": 2024,
        }
        response = self.client.post(self.books_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 2)
        self.assertEqual(Book.objects.get(isbn="9876543210123").title, "New Book")

    def test_update_book_status(self):
        data = {"available": False}
        response = self.client.patch(self.book_status_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.book.refresh_from_db()
        self.assertFalse(self.book.available)


class ReservationViewsTest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.client.force_authenticate(user=self.user)

        self.book = Book.objects.create(
            title="Test Book", author="Test Author", isbn="1234567890123"
        )

        self.reservation = Reservation.objects.create(
            book=self.book, user=self.user, status="pending"
        )

        self.reservation_url = reverse(
            "library_app:v1:reservation-detail", args=[self.reservation.id]
        )
        self.reservations_url = reverse("library_app:v1:reservation-list")

    def test_get_reservation_list(self):
        response = self.client.get(self.reservations_url)
        reservations = Reservation.objects.all()
        serializer = ReservationSerializer(reservations, many=True)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["results"], serializer.data)

    def test_get_reservation_detail(self):
        response = self.client.get(self.reservation_url)
        serializer = ReservationSerializer(self.reservation)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data, serializer.data)

    def test_create_reservation(self):
        book2 = Book.objects.create(
            title="Another Book", author="Another Author", isbn="9876543210123"
        )

        data = {"book": book2.id, "status": "pending"}
        response = self.client.post(self.reservations_url, data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Reservation.objects.count(), 2)
        self.assertEqual(Reservation.objects.get(book=book2).user, self.user)

    def test_update_reservation_status(self):
        data = {"status": "confirmed"}
        response = self.client.patch(self.reservation_url, data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.reservation.refresh_from_db()
        self.assertEqual(self.reservation.status, "confirmed")
