# pure settings purposes
def change_language(default: str = "cz") -> dict:
    if default == 'en':
        return {
            "position": "Enter position",
            "timespan": "Enter timespan",
            "control": "confirm",
            "latitude": "latitude",
            "longitude": "longitude",
            "date_actual": "current time",
            "date_from": "start time",
            "date_to": "end time",
            "run": "run calculation"
        }
    elif default == 'de':
        return {
            "position": "Position eingeben",
            "timespan": "Zeitraum eingeben",
            "control": "bestätigen",
            "latitude": "Breitengrad",
            "longitude": "Längengrad",
            "date_actual": "Aktualzeit",
            "date_from": "Startzeit",
            "date_to": "Endzeit",
            "run": "Berechnung ausführen"
        }
    elif default == 'es':
        return {
            "position": "Ingrese posición",
            "timespan": "Ingrese rango de tiempo",
            "control": "confirmar",
            "latitude": "latitud",
            "longitude": "longitud",
            "date_actual": "hora de actual",
            "date_from": "hora de inicio",
            "date_to": "hora de fin",
            "run": "ejecutar cálculo"
        }
    elif default == 'fr':
        return {
            "position": "Entrez la position",
            "timespan": "Entrez la période",
            "control": "confirmer",
            "latitude": "latitude",
            "longitude": "longitude",
            "date_actual": "heure aktuel",
            "date_from": "heure de début",
            "date_to": "heure de fin",
            "run": "lancer le calcul"
        }
    else:
        return {
            "position": "Zadejte pozici",
            "timespan": "Zadejte časové rozmezí",
            "control": "potvrdit",
            "latitude": "zeměpisná šířka",
            "longitude": "zeměpisná délka",
            "date_actual": "aktuální čas",
            "date_from": "počátěční čas",
            "date_to": "koncový čas",
            "run": "spustit výpočet"
        }


if __name__ == "__main__":
    # simple dummy test
    t = change_language("cz")
    # print(t["display"])
