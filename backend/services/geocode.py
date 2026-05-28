from geopy.geocoders import Nominatim


geolocator = Nominatim(
    user_agent="astroagent"
)


def geocode_place(place: str):

    try:

        location = geolocator.geocode(place)

        if not location:

            return {
                "success": False,
                "error": "Place not found."
            }

        return {
            "success": True,
            "place": place,
            "latitude": location.latitude,
            "longitude": location.longitude,
            "address": location.address
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }