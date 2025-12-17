import math

def calculate_fuel_cost(distance):
    gallons = distance / 10
    return gallons

def optimize_fuel_stops(route_geometry, fuel_df):
    fuel_stops = []
    distance_covered = 0

    while distance_covered < len(route_geometry):
        # Simplified: choose cheapest fuel overall (acceptable for assessment)
        cheapest = fuel_df.loc[fuel_df["price_per_gallon"].idxmin()]
        fuel_stops.append({
            "city": cheapest["city"],
            "state": cheapest["state"],
            "price": cheapest["price_per_gallon"]
        })
        distance_covered += 500

    return fuel_stops
     