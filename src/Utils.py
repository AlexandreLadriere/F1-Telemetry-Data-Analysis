import pandas
import fastf1
import numpy as np

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

def get_sectors_position(lap: fastf1.core.Lap):
        '''Get position (in meters) for each sector limit

        Keyword arguments:
        lap - The lap for which you want to get the sectors position
        '''
        lap_telemetry = lap.get_car_data().add_distance()
        sector12 = lap_telemetry['Distance'].iloc[np.argmin(abs(lap_telemetry['SessionTime'] - lap['Sector1SessionTime']))]
        sector23 = lap_telemetry['Distance'].iloc[np.argmin(abs(lap_telemetry['SessionTime'] - lap['Sector2SessionTime']))]
        return sector12, sector23