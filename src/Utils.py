import pandas
import fastf1
import numpy as np
from datetime import timedelta

DICT_COMPOUND = {'SOFT': 'S', 'MEDIUM': 'M', 'HARD': 'H'}

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
    """Get position (in meters) for each sector limit

    Keyword arguments:
    lap - The lap for which you want to get the sectors position
    """
    lap_telemetry = lap.get_car_data().add_distance()
    sector12 = lap_telemetry['Distance'].iloc[np.argmin(abs(lap_telemetry['SessionTime'] - lap['Sector1SessionTime']))]
    sector23 = lap_telemetry['Distance'].iloc[np.argmin(abs(lap_telemetry['SessionTime'] - lap['Sector2SessionTime']))]
    return sector12, sector23

def get_drivers_color(driver_list):
    """Get a list of color for a given list of driver

    Keyword arguments:
    driver_list   -- List of drivers names
    """
    colors = []
    for pilot in driver_list:
        colors.append(fastf1.plotting.driver_color(pilot))
    return colors

def get_fastest_laps(session: fastf1.core.Session):
    """Get the fastest lap for each pilot in the given session (list)

    Keyword arguments:
    session -- Session for wich you want to get all pilots fastest lap
    """
    drivers_fastest_lap = []
    drivers_numbers = session.drivers
    for driver in drivers_numbers:
        fast_lap = session.laps.pick_driver(driver).pick_fastest()
        drivers_fastest_lap.append(fast_lap)
    return drivers_fastest_lap

def get_drivers_fastest_lap(session: fastf1.core.Session, drivers: list[str]):
    """Get the fastest lap for each given pilot in the given session (list)

    Keyword arguments:
    session -- Session for wich you want to get all pilots fastest lap
    drivers -- List of all drivers name
    """
    drivers_fastest_lap = []
    for driver in drivers:
        fast_lap = session.laps.pick_driver(driver).pick_fastest()
        drivers_fastest_lap.append(fast_lap)
    return drivers_fastest_lap

def get107Time(quali_session: fastf1.core.Session):
    """Get the 107% time for qualification (107% time is determined from Q1)

    Keyword arguments:
    quali_session -- Qualifying session for which you want to get the 107% time
    """
    #get all session results
    results = quali_session.results
    min = results['Q1'][0]
    for index, row in results.iterrows():
        if row['Q1'] < min:
            min = row['Q1']
    min_s = min.total_seconds()
    time_107_s = min_s * 1.07
    return timedelta(seconds=time_107_s)