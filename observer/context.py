from datetime import datetime, timedelta
import pandas as pd
import pydeck as pdk
from skyfield.api import load, Topos, utc
from skyfield import timelib
import sqlite3


class Master:
    def __init__(self, source_file: str = "./source/de430.bsp", located: str = "", date_format="'%Y-%m-%d %H:%M'"):
        # Initiates center
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
            "gran": '',
            "format": date_format,
            "frame": None  # this will hold pandas time frame
        }

    def move_head_location(self, x: int = 0, y: int = 0, planet=""):
        # very simplified shifting function
        if planet:
            return self.planets[planet]
        elif pd.isna(x) and pd.isna(y):
            return self.planets['earth']  # default one
        else:
            return self.planets['earth'] + Topos(f'{x} N', f'{y} E')

    def move_head_direction(self, *args):
        self.head["direction"] = [obj for obj in args if obj in self.available.values()]

    def frame_the_time(self, what: str = "", year: int = 0, month: int = 0, day: int = 0, hour: int = 0,
                       minute: int = 0):
        if not what:  # hardcoded current month with daily granularity
            self.time["from"] = self.time["scale"].now().utc_strftime()
            self.time["to"] = (self.time["scale"].now() + timedelta(days=1 * 30)).utc_strftime()
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

    def frame_prepare(self) -> pd.DataFrame:
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
                    df[f"{planet}_distance"] = df['date_time'].apply(self.distance, args=(planet,))
                elif "dec" in computation:
                    df[f"{planet}_declination"] = df['date_time'].apply(self.degrees, args=(planet,))
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
            return self.time["scale"].utc(ts_object.year, ts_object.month, ts_object.day, ts_object.hour,
                                          ts_object.minute)
        else:
            return ts_object  # no change


class Computation:
    # Extra class serves as backup
    def __init__(self, c, o):
        self.centerpoint = c
        self.observed = o
        self.c = c
        self.ts = load.timescale()

    def shift(self, x=0, y=0):
        if pd.isna(x) and pd.isna(y):
            self.centerpoint = self.c
        else:
            self.centerpoint = self.c + Topos(f'{x} N', f'{y} E')


def planets_df() -> pd.DataFrame:
    return pd.DataFrame(
        {
            "planet": ["moon", "mercury", "venus", "mars", "jupiter", "saturn", "uran", "neptune", "pluto"],
            "selected": [True, False, False, False, True, True, True, True, True],
        }
    )


def loc_df(lat: int, lon: int) -> pd.DataFrame:
    return pd.DataFrame(
        {
            'latitude': [lat, ],
            'longitude': [lon, ],
            'color': ['#0044ff', ],
            'size': [10]
        },
        index=[1, ]
    )


def frequency(day: object = 0, hour: object = 0, minute: object = 0) -> str:
    if minute:
        return f'{minute}min'
    elif hour:
        return f'{60 * hour}min'
    elif day:
        return f'{1440 * day}min'  # x day timestep


########### BACKUP ###########
def degrees(t):
    # %t%: timestamp value
    return sel.centerpoint.at(format_time(t)).observe(sel.observed).radec()[1].degrees


def distance(t):
    # %t%: timestamp value
    return sel.centerpoint.at(format_time(t)).observe(sel.observed).radec()[-1].au


def observer(start, end, gran):
    """iteration that computes values for given parameters
    %c%: center point position (with Topos module or another) 
    %start%: start date (pandas dataframe row)
    %end%: end date (pandas dataframe row)
    %gran%: granularity (pandas dataframe row)
    returns pandas dataframe
    """
    if not isinstance(start, pd.DataFrame) or not isinstance(end, pd.DataFrame) or not isinstance(gran, pd.DataFrame):
        return
    print(f"""      from {start.Day.iloc[0]}/{start.Month.iloc[0]}/{start.Year.iloc[0]} 
        to {end.Day.iloc[0]}/{end.Month.iloc[0]}/{end.Year.iloc[0]} 
        at time step {gran.Day.iloc[0]} days {gran.Hour.iloc[0]} hours {gran.Minute.iloc[0]} minutes""")
    time_span = pd.date_range(f'{start.Month.iloc[0]}/{start.Day.iloc[0]}/{start.Year.iloc[0]}',
                              f'{end.Month.iloc[0]}/{end.Day.iloc[0]}/{end.Year.iloc[0]}',
                              freq=frequency(gran.Day.iloc[0], gran.Hour.iloc[0], gran.Minute.iloc[0]))

    obs = pd.DataFrame(time_span, columns=['date_time'])
    obs['declination'] = obs['date_time'].apply(degrees)
    obs['distance'] = obs['date_time'].apply(distance)

    return obs


def load_db_setup(location="./settings.db", table="TimePeriod"):
    with sqlite3.connect(location) as db_connection:
        return pd.read_sql(f"SELECT * FROM {table};", db_connection)


def generate_result_files():
    variants = load_db_setup(table="ComputeVariants")
    time_period = load_db_setup(table="TimePeriod")
    labels = variants[variants.columns[[2, 3, 4]]].apply(lambda x: f'{list(x)[0]} ({list(x)[1]} / {list(x)[2]})',
                                                         1).tolist()

    sel = Computation(planets['earth'], planets['moon'])

    start_point = time_period['Param'] == 'start_point'
    end_point = time_period['Param'] == 'end_point'
    granularity = time_period['Param'] == 'granularity'

    for idx, var in variants.iterrows():
        if not pd.isna(var[3]):
            sel.shift(var[3], var[4])
        print(f'computing variant {var[1]} {labels[idx]}')
        o = observer(time_period[start_point], time_period[end_point], time_period[granularity])
        print(f'      output to file ./result/{var[-1]}')
        o.to_csv('./result/' + var[-1], index=False, mode='w')


def now():
    return datetime.now()
