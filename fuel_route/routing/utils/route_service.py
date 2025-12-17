import requests
import os
import math

ORS_API_KEY = os.getenv("ORS_API_KEY")

MILES_PER_GALLON = 10
MAX_RANGE_MILES = 500


def get_route(start, end):
    url = "https://api.openrouteservice.org/v2/directions/driving-car/geojson"

    headers = {
        "Authorization": ORS_API_KEY,
        "Content-Type": "application/json",
    }

    body = {
        "coordinates": [
            start,
            end
        ]
    }

    response = requests.post(url, json=body, headers=headers)
    data = response.json()

    if "features" not in data:
        raise Exception(f"Routing API error: {data}")

    segment = data["features"][0]["properties"]["segments"][0]

    distance_miles = segment["distance"] * 0.000621371
    geometry = data["features"][0]["geometry"]["coordinates"]

    fuel_needed_gallons = distance_miles / MILES_PER_GALLON

    fuel_stops_required = max(
        math.ceil(distance_miles / MAX_RANGE_MILES) - 1,
        0
    )

    return {
        "distance_miles": round(distance_miles, 2),
        "fuel_needed_gallons": round(fuel_needed_gallons, 2),
        "fuel_stops_required": fuel_stops_required,
        "route_geometry": geometry
    }

print("ORS API KEY LOADED:", bool(ORS_API_KEY))
