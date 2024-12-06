import json
from os import path

current_directory = path.dirname(__file__)


def get_locale_by_country_code(country_code: str) -> str:
    with open(path.join(current_directory, "locales.json"), "r") as file:
        content = json.load(file)
        locales = content.get(country_code.upper(), "en_US")
        return locales
