import fastf1
import fastf1.plotting
import pandas as pd
import numpy as np


from matplotlib import pyplot as plt
from matplotlib import cm
from matplotlib.collections import LineCollection

fastf1.plotting.setup_mpl()

MINISECTORS = 20

# see https://medium.com/towards-formula-1-analysis/analyzing-formula-1-data-using-python-2021-abu-dhabi-gp-minisector-comparison-3d72aa39e5e8

class LapDominance:
    def plot(self, session: fastf1.core.Session):
        """Plot the lap dominance by minisectors based on all pilots in the given session
        
        Keyword arguments:
        session -- Session for wich you want to plot the lap dominance
        """
        ### Does not work correctly dur to inconsistency in position data for each driver of the given session
        session.load()
        drivers_fastest_laps = self.__get_drivers_fastest_lap(session)
        drivers_fastest_laps_telemetry = self.__get_telemetry_from_lap_list(drivers_fastest_laps)
        merged_telemetry = self.__merging_telemetry(drivers_fastest_laps_telemetry)
        merged_telemetry_with_minisectors = self.__create_minisectors(merged_telemetry)
        merged_telemetry_with_minisectors_and_fastest_driver = self.__get_fastest_driver_by_minisector(merged_telemetry_with_minisectors)
        self.plot_fastest_driver_by_minisector(merged_telemetry_with_minisectors_and_fastest_driver)
        return 
    
    def plot_comparison(self, session: fastf1.core.Session, drivers: list[str]):
        """Plot the lap dominance by minisectors based on all the given pilots
        
        Keyword arguments:
        session -- Session for wich you want to plot the lap dominance
        drivers -- List of all drivers name
        """
        session.load()
        drivers_fastest_laps = self.__get_drivers_fastest_lap(session, drivers)
        drivers_fastest_laps_telemetry = self.__get_telemetry_from_lap_list(drivers_fastest_laps)
        merged_telemetry = self.__merging_telemetry(drivers_fastest_laps_telemetry)
        merged_telemetry_with_minisectors = self.__create_minisectors(merged_telemetry)
        merged_telemetry_with_minisectors_and_fastest_driver = self.__get_fastest_driver_by_minisector(merged_telemetry_with_minisectors)
        self.plot_fastest_driver_by_minisector(merged_telemetry_with_minisectors_and_fastest_driver)
        return

    def __get_drivers_fastest_lap(self, session: fastf1.core.Session):
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
    
    def __get_drivers_fastest_lap(self, session: fastf1.core.Session, drivers: list[str]):
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
    
    def __get_telemetry_from_lap_list(self, laps_list: list[fastf1.core.Lap]):
        """Get the telemetry for each lap in the given list

        Keyword arguments:
        laps_list -- List of all thee lap forwich you want to get the telemtry (with distance field)
        """
        laps_telemetry = []
        for lap in laps_list:
            tmp_fastest=lap.get_telemetry().add_distance()
            #adding driver to field to the telemetry
            tmp_fastest['Driver'] = lap['Driver']
            tmp_fastest['Driver_num'] = lap['DriverNumber']
            laps_telemetry.append(tmp_fastest)
        return laps_telemetry
    
    def __merging_telemetry(self, telemetry_list: list[fastf1.core.Telemetry]):
        """Merge all the given DataFrames in one

        Keyword arguments:
        telemetry_list  -- List of all the telemetry DataFrames you want to merge
        """
        global_telemetry = telemetry_list[0]
        for i in range(1, len(telemetry_list), 1):
            global_telemetry = pd.concat([global_telemetry, telemetry_list[i]], axis=0, ignore_index=False)
        return global_telemetry
    
    def __create_minisectors(self, telemetry: fastf1.core.Telemetry):
        """Create and assign minisectors for each row in the given fastf1.core.Telemetry DataFrame
        The number of miniseectors is defined by MINISECTORS

        Keyword arguments:
        telemetry  -- Telemetry DataFrame for which you want to assign minisectors
        """
        total_distance = max(telemetry['Distance'])
        minisector_length = total_distance / MINISECTORS
        minisectors = [0]
        #list of all the distance at which a minisector starts
        for i in range(0, (MINISECTORS - 1)):
            minisectors.append(minisector_length * (i + 1))
        """
        #assign minisector for each row in telemetry dataframe
        telemetry['Minisector'] = telemetry['Distance'].apply(
            lambda dist: (
                int((dist // minisector_length) + 1)
            )
        )
        """
        telemetry['Minisector'] =  telemetry['Distance'].apply(
            lambda z: (
                minisectors.index(
                min(minisectors, key=lambda x: abs(x-z)))+1
            )
        )

        return telemetry
    
    def __get_fastest_driver_by_minisector(self, telemetry: fastf1.core.Telemetry):
        """Get the fastest driver for each mini sector and link it with the global telemetry dataframe

        Keyword arguments:
        telemetry  -- Telemetry DataFrame for which you want to get the fastest driver by mini sector
        """
        #calculate average speed per driver per minisector
        average_speed = telemetry.groupby(['Minisector', 'Driver', 'Driver_num'])['Speed'].mean().reset_index()
        #select the fastest driver for each minisector
        fastest_driver = average_speed.loc[average_speed.groupby(['Minisector'])['Speed'].idxmax()]
        # Get rid of the speed column and rename the driver column
        fastest_driver = fastest_driver[['Minisector', 'Driver', 'Driver_num']].rename(columns={'Driver': 'Fastest_driver', 'Driver_num': 'Fastest_driver_num'})
        # Join the fastest driver per minisector with the full telemetry
        telemetry = telemetry.merge(fastest_driver, on=['Minisector'])
        # Order the data by distance to make matploblib does not get confused
        telemetry = telemetry.sort_values(by=['Distance'])
        # Set an int for each driver. Will be used to plot fig at the end
        telemetry = self.__set_fastest_driver_int(telemetry)
        return telemetry
    
    def __set_fastest_driver_int(self, telemetry: fastf1.core.Telemetry):
        """Set an integer for each fastest driver per mini sector. These integers will be used to plot data at the end

        Keyword arguments:
        telemetry  -- Telemetry DataFrame for which you want to set a unique integers for each fastest driver per minisector
        """
        unique_fasest_driver = telemetry['Fastest_driver'].unique().tolist()
        for i in range(0, len(unique_fasest_driver), 1):
            telemetry.loc[telemetry['Fastest_driver'] == unique_fasest_driver[i], 'Fastest_driver_int'] = i + 1
        return telemetry

    def plot_fastest_driver_by_minisector(self, telemetry: fastf1.core.Telemetry):
        fig, ax = plt.subplots(sharex=True, sharey=True)
        x = np.array(telemetry['X'].values)
        y = np.array(telemetry['Y'].values)

        points = np.array([x, y]).T.reshape(-1, 1, 2)
        segments = np.concatenate([points[:-1], points[1:]], axis=1)
        fastest_driver_array = telemetry['Fastest_driver_int'].to_numpy().astype(float)
        cmap = cm.get_cmap('winter', 2)
        lc_comp = LineCollection(segments, norm=plt.Normalize(1, cmap.N+1), cmap=cmap)
        lc_comp.set_array(fastest_driver_array)
        lc_comp.set_linewidth(1)
        plt.gca().add_collection(lc_comp)
        plt.axis('equal')
        plt.tick_params(labelleft=False, left=False, labelbottom=False, bottom=False)
        #cbar = plt.colorbar(mappable=lc_comp, boundaries=np.arange(1,4))
        #cbar.set_ticks(np.arange(1.5, 4.5))

        plt.show()
        return
