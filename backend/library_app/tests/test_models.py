# -*- coding: utf-8 -*-
import pytest
from django.test import TestCase
from library_app.models import Book, Reservation, SystemLog, User


class BookModelTest(TestCase):
    def setUp(self):
        self.book = Book.objects.create(
            title="Test Book",
            author="Test Author",
            isbn="1234567890123",
            publication_year=2024,
            available=True,
        )

    def test_book_creation(self):
        self.assertEqual(self.book.title, "Test Book")
        self.assertEqual(self.book.author, "Test Author")
        self.assertEqual(self.book.isbn, "1234567890123")
        self.assertEqual(self.book.publication_year, 2024)
        self.assertTrue(self.book.available)

    def test_book_str(self):
        self.assertEqual(str(self.book), "Test Book by Test Author")


class ReservationModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.book = Book.objects.create(
            title="Test Book", author="Test Author", isbn="1234567890123"
        )
        self.reservation = Reservation.objects.create(
            book=self.book, user=self.user, status="pending"
        )

    def test_reservation_creation(self):
        self.assertEqual(self.reservation.book, self.book)
        self.assertEqual(self.reservation.user, self.user)
        self.assertEqual(self.reservation.status, "pending")
        self.assertIsNotNone(self.reservation.reservation_date)
        self.assertIsNone(self.reservation.return_date)

    def test_reservation_str(self):
        expected = f"{self.book.title} reserved by {self.user.username}"
        self.assertEqual(str(self.reservation), expected)


class SystemLogModelTest(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="testuser", email="test@example.com", password="testpass123"
        )
        self.log = SystemLog.objects.create(
            level="INFO",
            message="Test log message",
            source="Test Source",
            user=self.user,
        )

    def test_log_creation(self):
        self.assertEqual(self.log.level, "INFO")
        self.assertEqual(self.log.message, "Test log message")
        self.assertEqual(self.log.source, "Test Source")
        self.assertEqual(self.log.user, self.user)
        self.assertIsNone(self.log.trace)

    def test_log_str(self):
        expected = f"[INFO] Test Source: Test log message..."
        self.assertEqual(str(self.log), expected)
