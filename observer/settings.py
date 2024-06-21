import pandas as pd
import sqlite3
from pathlib import Path


def change_language(default: str = "cz") -> dict:
    return {
        "position": "Zadejte pozici",
        "timespan": "Zadejte časové rozmezí",
        "control": "potvrdit",
        "latitude": "zeměpisná šířka",
        "longitude": "zeměpisná délka",
        "date_from": "počátěční čas",
        "date_to": "koncový čas",
        "run": "spustit výpočet"
    }


if __name__ == "__main__":
    t = change_language("cz")
    # print(t["display"])
