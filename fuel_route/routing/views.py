from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status

import requests
import os
import base64
import json
from .utils.route_service import get_route, MILES_PER_GALLON
from .utils.fuel_loader import get_fuel_data

@api_view(['POST'])
@permission_classes([AllowAny])
def route_with_fuel(request):
    data = request.data

    # -----------------------------
    # 1️⃣ Input validation
    # -----------------------------
    if "start" not in data or "end" not in data:
        return Response(
            {"error": "start and end coordinates are required"},
            status=status.HTTP_400_BAD_REQUEST
        )

    start = data["start"]
    end = data["end"]

    if (
        not isinstance(start, list)
        or not isinstance(end, list)
        or len(start) != 2
        or len(end) != 2
    ):
        return Response(
            {"error": "start and end must be [longitude, latitude]"},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        # -----------------------------
        # 2️⃣ Get route + distance
        # -----------------------------
        route_data = get_route(start, end)

        # -----------------------------
        # 3️⃣ Load fuel prices from CSV
        # -----------------------------
        fuel_data = get_fuel_data()

        if not fuel_data:
            return Response(
                {"error": "Fuel price data not available"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        # -----------------------------
        # 4️⃣ Optimal fuel stop logic
        # -----------------------------
        # Sort by cheapest price
        fuel_data_sorted = sorted(fuel_data, key=lambda x: x["price"])

        stops_needed = route_data["fuel_stops_required"]

        optimal_fuel_stops = fuel_data_sorted[:stops_needed]

        # -----------------------------
        # 5️⃣ Fuel cost calculation
        # -----------------------------
        total_fuel_needed = route_data["distance_miles"] / MILES_PER_GALLON

        if optimal_fuel_stops:
            avg_price = (
                sum(stop["price"] for stop in optimal_fuel_stops)
                / len(optimal_fuel_stops)
            )
        else:
            avg_price = fuel_data_sorted[0]["price"]

        total_fuel_cost = round(total_fuel_needed * avg_price, 2)

        # -----------------------------
        # 6️⃣ FINAL API RESPONSE
        # -----------------------------
        response = {
            "distance_miles": route_data["distance_miles"],
            "fuel_stops_required": stops_needed,
            "optimal_fuel_stops": optimal_fuel_stops,
            "total_fuel_cost_usd": total_fuel_cost,
            "route_geometry": route_data["route_geometry"]
        }

        return Response(response, status=status.HTTP_200_OK)

    except Exception as e:
        return Response(
            {"error": str(e)},
            status=status.HTTP_400_BAD_REQUEST
        )
        