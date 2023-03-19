import pandas
import fastf1

def get_str_lap_time_from_timedelta(time: pandas.Timedelta):
    """Get time (m:s:ms) in str from the given pandas.Timedelta object

    Keyword arguments:
    time    - pandas.Timedelta object from which you want to get time in str
    """
    return str(time)[10:19]

def get_str_lap_time_from_lap(lap: fastf1.core.Lap):
    """Get time (m:s:ms) in str from the given fastf1.core.Lap object

    Keyword arguments:
    lap    - fastf1.core.Lap object from which you want to get lap time in str
    """
    car_data = fastf1.core.Telemetry(lap.get_car_data())
    return str(car_data['Time'].iloc[-1])[10:19]