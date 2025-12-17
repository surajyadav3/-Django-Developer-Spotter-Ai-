from django.urls import path
from .views import route_with_fuel

urlpatterns = [
    path("route/", route_with_fuel, name="route_with_fuel"),
]
