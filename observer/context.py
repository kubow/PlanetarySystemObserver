from datetime import timedelta
import pandas as pd
from skyfield.api import load, Topos, utc
from skyfield import timelib
import sqlite3

class Master:
    def __init__(self, source_file: str="./source/de430.bsp", located: str="", format="'%Y-%m-%d %H:%M'"):
        self.planets = load(source_file)
        self.available = {0: "solar", 1: "mercury", 2: "venus", 3: "earth", 4: "mars",
                          5: "jupiter", 6: "saturn", 7: "uran", 8: "neptune", 9: "pluto", 
                          10: "sun", 199: "mercury", 299: "venus", 301: "moon", 399: "earth"}
        self.head = {
            "location": self.move_head_location(planet=located),
            "direction": ["planets", "list", "to be", "observed"],
            "compute": ["declination", ]  # "distance"
        }
        self.time = {
            "scale": load.timescale(),
            "from": 0,
            "to": 0,
            "gran": 0,
            "format": format,
            "frame" : None  # this will hold pandas time frame
        }
    
    def move_head_location(self, x: int=0, y: int=0, planet=""):
        # very simplified shifting function
        if planet:
            return self.planets[planet]
        elif pd.isna(x) and pd.isna(y):
            return self.planets['earth']  # default one
        else:
            return self.planets['earth'] + Topos(f'{x} N', f'{y} E')
    
    def move_head_direction(self, *args):
        self.head["direction"] = [obj for obj in args if obj in self.available.values()]
    
    def frame_the_time(self, what: str="", year: int=0, month: int=0, day: int=0, hour: int=0, minute: int=0):
        if not what:  # hardcoded current month with daily granularity
            self.time["from"] = self.time["scale"].now().utc_strftime()
            self.time["to"] = (self.time["scale"].now() + timedelta(days=1*30)).utc_strftime()
            self.time["gran"] = frequency(day=1)
            self.time["frame"] = self.frame_prepare()
        elif what == "gran":
            self.time["gran"] = frequency(year, month, day)
        elif what in ("from", "to"):
            self.time[what] = self.time["scale"].utc(year, month, day, hour, minute).utc_strftime()
        elif what == "frame":
            self.time["frame"] = self.frame_prepare()
        else:
            print("not known method...")

    def frame_prepare(self):
        df = pd.DataFrame(
            pd.date_range(
                self.time["from"], self.time["to"], 
                freq=self.time["gran"]
            ),
            columns=['date_time']
        )
        for planet in self.head["direction"]:
            for computation in self.head["compute"]:
                if computation == "distance":
                    df[f"{planet}_distance"] = df['date_time'].apply(self.distance, args=(planet, ))
                elif "dec" in computation:
                    df[f"{planet}_declination"] = df['date_time'].apply(self.degrees, args=(planet, ))
        return df
    
    def degrees(self, t, target):
        # %t%: timestamp value
        return self.head["location"].at(self.format_time(t)).observe(self.id(target)).radec()[1].degrees

    def distance(self, t, target):
        # %t%: timestamp value
        return self.head["location"].at(self.format_time(t)).observe(self.id(target)).radec()[-1].au
    
    def id(self, planet_name):
        for key, val in self.available.items():
            if val == planet_name:
                return self.planets[key]

    def format_time(self, ts_object):
        if isinstance(ts_object, timelib.Time):
            return ts_object.utc_strftime('%Y-%m-%d %H:%M')
        elif isinstance(ts_object, pd.Timestamp):
            return self.time["scale"].utc(ts_object.year, ts_object.month, ts_object.day, ts_object.hour, ts_object.minute)
        else:
            return ts_object  # no change

def planets_df():
    return pd.DataFrame(
        {
            "planet": ["moon", "mercury", "venus", "mars", "jupiter", "saturn", "uran", "neptune", "pluto"],
            "selected": [True, False, False, False, True, True, True, True, True],
        }
    )

def frequency(day=0, hour=0, minute=0):
    if minute:
        return f'{minute}min'
    elif hour:
        return f'{60*hour}min'
    elif day:
        return f'{1440*day}min' # x day timestep