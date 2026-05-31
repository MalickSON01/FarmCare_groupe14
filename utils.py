# utils.py
# This file contains reusable utility functions used throughout the project.
# These functions help with data validation and formatting.

from datetime import date
import re


def valider_nombre_entier(valeur: str, minimum: int = 1) -> bool:
    """Check that a string represents a valid integer.

    Args:
        valeur (str): The string to check.
        minimum (int): The minimum accepted value (default is 1).

    Returns:
        bool: True if the value is an integer >= minimum, False otherwise.
    """
    try:
        nombre = int(valeur)
        return nombre >= minimum
    except ValueError:
        return False


def valider_date(date_str: str) -> bool:
    """Check that a string is a valid date in YYYY-MM-DD format.

    Args:
        date_str (str): The date string to check (e.g. "2025-06-15").

    Returns:
        bool: True if the format and date are valid, False otherwise.
    """
    # Check the format using a simple regular expression
    modele = r"^\d{4}-\d{2}-\d{2}$"
    if not re.match(modele, date_str):
        return False

    # Check that the date actually exists in the calendar
    try:
        parties = date_str.split("-")
        date(int(parties[0]), int(parties[1]), int(parties[2]))
        return True
    except ValueError:
        return False


def formater_pourcentage(valeur: float) -> str:
    """Format a float as a readable percentage string.

    Args:
        valeur (float): The number to format.

    Returns:
        str: The formatted percentage (e.g. "4.50%").
    """
    return f"{valeur:.2f}%"


def date_aujourd_hui() -> str:
    """Return today's date in YYYY-MM-DD format.

    Returns:
        str: Today's date as a string.
    """
    return str(date.today())


def durees_disponibles() -> tuple:
    """Return the available cycle durations in days.

    Returns:
        tuple: A tuple of possible durations.
    """
    return (30, 45, 60, 90, 120, 180, 365)


def types_animaux_disponibles() -> list:
    """Return a list of common animal types.

    Returns:
        list: List of animal type names.
    """
    types = [
        "Chicken",
        "Sheep",
        "Goat",
        "Pig",
        "Cattle / Cow",
        "Rabbit",
        "Turkey",
        "Duck",
        "Other"
    ]
    return types

