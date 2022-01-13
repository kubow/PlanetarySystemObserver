"""This file is for testing purposes
Usage: just run for now
"""
import pandas as pd
from skyfield.api import load, Topos, utc
from skyfield import timelib
import sqlite3


class Computation:
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


def format_time(ts_object):
    if isinstance(ts_object, timelib.Time):
        return ts_object.utc_strftime('%Y-%m-%d %H:%M')
    elif isinstance(ts_object, pd.Timestamp):
        return sel.ts.utc(ts_object.year, ts_object.month, ts_object.day, ts_object.hour, ts_object.minute)
    else:
        return 

def degrees(t):
    # %t%: timestamp value
    return sel.centerpoint.at(format_time(t)).observe(sel.observed).radec()[1].degrees

def distance(t):
    # %t%: timestamp value
    return sel.centerpoint.at(format_time(t)).observe(sel.observed).radec()[-1].au
    
def frequency(day=0, hour=0, minute=0):
    if minute:
        return f'{minute}min'
    elif hour:
        return f'{60*hour}min'
    elif day:
        return f'{1440*day}min' # 1 day timestep

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


if __name__ == '__main__':
    db_connection = sqlite3.connect("./settings.db")
    variants = pd.read_sql("select * from ComputeVariants", db_connection)
    time_period = pd.read_sql("select * from TimePeriod", db_connection)
    labels = variants[variants.columns[[2,3,4]]].apply(lambda x: f'{list(x)[0]} ({list(x)[1]} / {list(x)[2]})', 1).tolist()

    planets = load('./source/de430.bsp')
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
        o.to_csv('./result/'+var[-1], index=False, mode='w')
        
    