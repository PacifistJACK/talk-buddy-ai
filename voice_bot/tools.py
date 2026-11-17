"""
Agent Tools
-----------
Python functions equipped with @tool for the LangChain agent to call.
"""

import xml.etree.ElementTree as ET
import requests
from langchain_core.tools import tool


@tool
def get_temperature(city: str) -> str:
    """
    Get the current temperature for a given city name.
    Use this whenever the user asks about weather or temperature.

    Args:
        city: Name of the city (e.g. "Mumbai", "London", "Tokyo")

    Returns:
        A string with the city name and its current temperature in Celsius.
    """
    geo = requests.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1},
        timeout=10,
    ).json()

    if not geo.get("results"):
        return f"Sorry, I couldn't find the city '{city}'."

    lat = geo["results"][0]["latitude"]
    lon = geo["results"][0]["longitude"]
    name = geo["results"][0]["name"]

    weather = requests.get(
        "https://api.open-meteo.com/v1/forecast",
        params={
            "latitude": lat,
            "longitude": lon,
            "current": "temperature_2m",
            "timezone": "auto",
        },
        timeout=10,
    ).json()

    temp = weather["current"]["temperature_2m"]
    return f"The current temperature in {name} is {temp}°C."


@tool
def get_latest_headlines(topic: str = "world") -> str:
    """
    Get the latest news headlines for a given topic or country.
    Use this whenever the user asks for news, headlines, or current events.

    Args:
        topic: The topic, category, or country (e.g. "technology", "sports", "India", "world")

    Returns:
        A formatted string with top 5 news headlines.
    """
    url = f"https://news.google.com/rss/search?q={topic}&hl=en&gl=US&ceid=US:en"
    headers = {"User-Agent": "Mozilla/5.0"}

    try:
        response = requests.get(url, headers=headers, timeout=5)
        root = ET.fromstring(response.content)
        items = root.findall(".//item")[:5]

        if not items:
            return f"No headlines found for '{topic}'."

        headlines = []
        for i, item in enumerate(items, 1):
            title = item.find("title")
            if title is not None and title.text:
                headlines.append(f"{i}. {title.text}")

        return f"Latest headlines for '{topic}':\n" + "\n".join(headlines)
    except Exception as e:
        return f"Could not fetch headlines at this moment: {e}"


# List of tools to pass into create_agent
ALL_TOOLS = [get_temperature, get_latest_headlines]

