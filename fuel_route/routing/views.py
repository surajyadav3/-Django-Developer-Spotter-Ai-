from rest_framework.decorators import api_view
from rest_framework.response import Response
import requests
import os


@api_view(["POST"])
def route_with_fuel(request):
    # ✅ MUST use request.data (NOT request.body)
    data = request.data

    start = data.get("start")
    end = data.get("end")

    if not start or not end:
        return Response(
            {"error": "start and end coordinates required"},
            status=400
        )

    ors_api_key = os.getenv("ORS_API_KEY")

    if not ors_api_key:
        return Response(
            {"error": "ORS API key not found"},
            status=500
        )

    ors_url = "https://api.openrouteservice.org/v2/directions/driving-car"

    headers = {
        "Authorization": ors_api_key,
        "Content-Type": "application/json"
    }

    payload = {
        "coordinates": [
            start,  # [lon, lat]
            end
        ]
    }

    ors_response = requests.post(
        ors_url,
        json=payload,
        headers=headers
    )

    return Response(ors_response.json())
