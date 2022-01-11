"""This file is for testing purposes
Usage: just run for now
"""

from calendar import monthrange
import pandas as pd
from skyfield.api import load, Topos
from skyfield import timelib
import sqlite3

def format_time(ts_object):
    if not isinstance(ts_object, timelib.Time):
        return
    else:
        return ts_object.utc_strftime('%Y-%m-%d %H:%M')

def listed_val(time_val, observation):
    return [time_val, observation.radec()[1].degrees, observation.radec()[-1].au]
    
def observer(c, start, end, gran):
    """iteration that computes values for given parameters
    %c%: center point position (with Topos module)
    %start%: start date (pandas dataframe row)
    %end%: end date (pandas dataframe row)
    %gran%: granularity (pandas dataframe row)
    returns pandas dataframe
    """
    if not isinstance(start, pd.DataFrame) or not isinstance(end, pd.DataFrame) or not isinstance(gran, pd.DataFrame):
        return
    ts = load.timescale()
    data = []
    print(f"""      from {start.Day.iloc[0]}/{start.Month.iloc[0]}/{start.Year.iloc[0]} 
        to {end.Day.iloc[0]}/{end.Month.iloc[0]}/{end.Year.iloc[0]} 
        at time step {gran.Day.iloc[0]} days {gran.Hour.iloc[0]} hours {gran.Minute.iloc[0]} minutes""")
    for year in range(start.Year.iloc[0], end.Year.iloc[0]+1):
        for month in range(start.Month.iloc[0], end.Month.iloc[0]+1):
            day_finish = monthrange(year, month)[1]  # or end.Day.iloc[0]
            for day in range(start.Day.iloc[0], day_finish + 1):
                if gran.Hour.iloc[0] or gran.Minute.iloc[0]:
                    for hour in range(1, 25):
                        if gran.Minute.iloc[0]:
                            for minute in range(1, 61):
                                t = ts.utc(year, month, day, hour, minute)
                                data.append(listed_val(format_time(t), c.at(t).observe(moon)))
                        else:  # case hourly reporting at 0 minutes 
                            t = ts.utc(year, month, day, hour)
                            data.append(listed_val(format_time(t), c.at(t).observe(moon)))
                else:  # case daily reporting at 12:00 every day
                    t = ts.utc(year, month, day, 12)
                    data.append(listed_val(format_time(t), c.at(t).observe(moon)))
    return pd.DataFrame(data, columns=['date_time', 'declination', 'distance'])


if __name__ == '__main__':
    db_connection = sqlite3.connect("./settings.db")
    variants = pd.read_sql("select * from ComputeVariants", db_connection)
    time_period = pd.read_sql("select * from TimePeriod", db_connection)
    labels = variants[variants.columns[[2,3,4]]].apply(lambda x: f'{list(x)[0]} ({list(x)[1]} / {list(x)[2]})', 1).tolist()

    planets = load('./source/de430.bsp')
    moon = planets['moon']  # observed point
    
    for idx, var in variants.iterrows():
        if pd.isna(var[3]):
            earth = planets['earth']
        else:
            earth = planets['earth'] + Topos(f'{var[3]} N', f'{var[4]} E')
        print(f'computing variant {var[1]} {labels[idx]}')
        start_point = time_period[time_period['Param'] == 'start_point']
        end_point = time_period[time_period['Param'] == 'end_point']
        granularity = time_period[time_period['Param'] == 'granularity']
        o = observer(earth, start_point, end_point, granularity)
        print(f'      output to file ./result/{var[-1]}')
        o.to_csv('./result/'+var[-1], index=False, mode='w')
        
    