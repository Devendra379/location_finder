import requests
import math


def get_coordinates_from_address(address):
    """Fetch latitude and longitude for an address using OpenStreetMap Nominatim API"""
    url = f"https://nominatim.openstreetmap.org/search?q={address}, India&format=json&limit=1"
    headers = {"User-Agent": "GeoSearchApp/1.0"}
    response = requests.get(url, headers=headers)
    data = response.json()

    if data:
        return float(data[0]["lat"]), float(data[0]["lon"])
    else:
        print("❌ No location found for this address.")
        return None, None


def haversine(lat1, lon1, lat2, lon2):
    """Calculate the Haversine distance between two coordinates"""
    R = 6371  # Earth radius in km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return R * c


def get_nearby_sorted_places(address, radius=5000):
    """Fetch nearby areas (not small localities) using Overpass API"""

    # Get lat/lon from address
    lat, lng = get_coordinates_from_address(address)
    if lat is None or lng is None:
        return []

    overpass_url = "https://overpass-api.de/api/interpreter"

    query = f"""
    [out:json];
    node
      (around:{radius},{lat},{lng})
      ["place"~"neighbourhood|suburb|borough"];
    out body;
    """

    response = requests.get(overpass_url, params={"data": query})
    data = response.json()

    areas = []
    if "elements" in data:
        for element in data["elements"]:
            if "tags" in element and "name" in element["tags"] and "lat" in element and "lon" in element:
                area_name = element["tags"]["name"]
                area_lat = float(element["lat"])
                area_lon = float(element["lon"])
                distance = haversine(lat, lng, area_lat, area_lon)
                areas.append((area_name, distance))

    # Sort areas by distance
    areas.sort(key=lambda x: x[1])
    return areas