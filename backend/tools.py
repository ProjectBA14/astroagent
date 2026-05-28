from langchain.tools import tool

from services.geocode import geocode_place

from services.astrology import (
    get_planet_positions,
    get_chart_svg
)


@tool
def geocode_place_tool(place: str):
    """
    Convert a birthplace into latitude and longitude.
    Use this whenever location coordinates are needed.
    """

    result = geocode_place(place)

    return result


@tool
def compute_birth_chart_tool(
    birth_date: str,
    birth_time: str,
    birth_place: str
):
    """
    Compute a compact Vedic astrology birth chart summary.
    Returns only the key planetary sign placements
    needed for reasoning.
    """

    geo = geocode_place(birth_place)

    if not geo["success"]:

        return {
            "success": False,
            "error": geo["error"]
        }

    result = get_planet_positions(
        birth_date=birth_date,
        birth_time=birth_time,
        latitude=geo["latitude"],
        longitude=geo["longitude"]
    )

    if not result["success"]:

        return result

    planet_data = result["data"]["data"]["planet_position"]

    compact_chart = {}

    for planet in planet_data:

        name = planet["name"]

        sign = planet["rasi"]["name"]

        compact_chart[name] = sign

    return {
        "success": True,
        "chart_summary": compact_chart
    }


@tool
def generate_chart_svg_tool(
    birth_date: str,
    birth_time: str,
    birth_place: str
):
    """
    Generate a South Indian style astrology chart SVG.
    Useful for frontend chart rendering.
    """

    geo = geocode_place(birth_place)

    if not geo["success"]:

        return {
            "success": False,
            "error": geo["error"]
        }

    result = get_chart_svg(
        birth_date=birth_date,
        birth_time=birth_time,
        latitude=geo["latitude"],
        longitude=geo["longitude"]
    )

    return result