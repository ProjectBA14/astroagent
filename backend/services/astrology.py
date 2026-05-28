import base64
import httpx

from config import (
    PROKERALA_CLIENT_ID,
    PROKERALA_CLIENT_SECRET
)

BASE_URL = "https://api.prokerala.com/v2"


def get_access_token():

    credentials = (
        f"{PROKERALA_CLIENT_ID}:"
        f"{PROKERALA_CLIENT_SECRET}"
    )

    encoded_credentials = base64.b64encode(
        credentials.encode()
    ).decode()

    headers = {
        "Authorization": f"Basic {encoded_credentials}"
    }

    data = {
        "grant_type": "client_credentials"
    }

    response = httpx.post(
        "https://api.prokerala.com/token",
        headers=headers,
        data=data
    )

    token_data = response.json()

    return token_data["access_token"]


def get_planet_positions(
    birth_date: str,
    birth_time: str,
    latitude: float,
    longitude: float,
    timezone: str = "+05:30"
):

    try:

        token = get_access_token()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {

            "datetime":
            f"{birth_date}T{birth_time}:00{timezone}",

            "coordinates":
            f"{latitude},{longitude}",

            "ayanamsa": 1
        }

        response = httpx.get(
            f"{BASE_URL}/astrology/planet-position",
            headers=headers,
            params=params
        )


        return {
            "success": True,
            "data": response.json()
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }


def get_chart_svg(
    birth_date: str,
    birth_time: str,
    latitude: float,
    longitude: float,
    timezone: str = "+05:30"
):

    try:

        token = get_access_token()

        headers = {
            "Authorization": f"Bearer {token}"
        }

        params = {

            "datetime":
            f"{birth_date}T{birth_time}:00{timezone}",

            "coordinates":
            f"{latitude},{longitude}",

            "ayanamsa": 1,

            "chart_type": "rasi",

            "chart_style": "south-indian"
        }

        response = httpx.get(
            f"{BASE_URL}/astrology/chart",
            headers=headers,
            params=params
        )

        return {
            "success": True,
            "data": response.text
        }

    except Exception as e:

        return {
            "success": False,
            "error": str(e)
        }