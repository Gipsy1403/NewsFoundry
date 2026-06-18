from datetime import datetime

# Liste des mois en français
FRENCH_MONTHS = [
    "janvier", "février", "mars", "avril", "mai", "juin",
    "juillet", "août", "septembre", "octobre", "novembre", "décembre"
]


def format_french_date(date: datetime) -> str:
    """
    Convertit une date en format français lisible.
    Exemple : 18 juin 2026
    """

    day = date.day
    month = FRENCH_MONTHS[date.month - 1]
    year = date.year

    return f"{day:02d} {month} {year}"