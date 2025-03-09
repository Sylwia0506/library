from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

app_name = "library_app"

v1_patterns = [
    path("books/", views.BookListView.as_view(), name="book-list"),
    path("books/<int:pk>/", views.BookDetailView.as_view(), name="book-detail"),
    path("books/<int:pk>/status/", views.BookStatusView.as_view(), name="book-status"),
    path("reservations/", views.ReservationListView.as_view(), name="reservation-list"),
    path(
        "reservations/<int:pk>/",
        views.ReservationDetailView.as_view(),
        name="reservation-detail",
    ),
]

urlpatterns = [
    path("v1/", include((v1_patterns, "v1"))),
]
