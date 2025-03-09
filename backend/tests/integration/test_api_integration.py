import pytest
from library_app.models import Book, User
from rest_framework.test import APIClient


@pytest.fixture
@pytest.mark.django_db
def api_client():
    user = User.objects.create_user(username="testuser", password="testpass123")
    client = APIClient()
    client.force_authenticate(user=user)
    return client


@pytest.fixture
@pytest.mark.django_db
def book():
    return Book.objects.create(
        title="Test Book", author="Test Author", isbn="1234567890"
    )


@pytest.mark.django_db
def test_check_book_availability(api_client, book, requests_mock):
    external_api_url = f"http://http://external-library-1.com/api/books/{book.isbn}/availability"

    requests_mock.get(external_api_url, json={"status": "available"}, status_code=200)

    url = f"/v1/books/{book.id}/status/"
    response = api_client.get(url)

    assert response.status_code == 200
    assert response.data["external_status"] == "available"
    assert response.data["book_id"] == book.id
