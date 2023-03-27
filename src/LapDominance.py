import fastf1
import fastf1.plotting

from matplotlib import pyplot as plt
fastf1.plotting.setup_mpl()

# see https://medium.com/towards-formula-1-analysis/analyzing-formula-1-data-using-python-2021-abu-dhabi-gp-minisector-comparison-3d72aa39e5e8

class LapDominance:
    def plot(self, session: fastf1.core.Session):
        session.load()
        drivers_fastest_laps = self.__get_drivers_fastest_lap(session)
        drivers_fastest_laps_telemetry = self.__get_telemetry_from_lap_list(drivers_fastest_laps)
        print(drivers_fastest_laps_telemetry[14]['Distance'][23])
        return 
    
    def __get_drivers_fastest_lap(self, session: fastf1.core.Session):
        drivers_fastest_lap = []
        drivers_numbers = session.drivers
        for driver in drivers_numbers:
            fast_lap = session.laps.pick_driver(driver).pick_fastest()
            drivers_fastest_lap.append(fast_lap)
        return drivers_fastest_lap
    
    def __get_telemetry_from_lap_list(self, laps_list: list[fastf1.core.Lap]):
        laps_telemetry = []
        for lap in laps_list:
            laps_telemetry.append(lap.get_car_data().add_distance())
        return laps_telemetry