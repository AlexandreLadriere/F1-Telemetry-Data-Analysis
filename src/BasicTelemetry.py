import fastf1
import fastf1.plotting
import Utils

from matplotlib import pyplot as plt
import matplotlib.patches as mpatches
fastf1.plotting.setup_mpl()

class BasicTelemetry:
    __SECTOR_COLOR = 'y'
    __SECTOR_ALPHA = 0.8
    __DISTANCE_MAX = 0
    __pilot_patch = []

    def plot(self, lap: fastf1.core.Lap, pilot: str, lap_name: str):
        """Plot basic telemetry data (Speed, RPM, Gear, Throttle, Break) for the given pilot on the given lap

        Keyword arguments:
        lap         -- The lap for which you want to plot telemetry data
        pilot       -- The name of the pilot who made the lap
        lap_name    -- The name you want to give to the lap (will be in the graph title)
        """
        fig, axes = self.__init_graph()
        car_data = fastf1.core.Telemetry(lap.get_car_data().add_distance())
        pilot_color = fastf1.plotting.driver_color(pilot)
        fig = self.__plot_data(fig, car_data, pilot_color, pilot)
        fig = self.__plot_max_speed(fig, car_data, pilot_color)
        self.__pilot_patch.append(self.__get_pilot_patch(pilot=pilot, pilot_color=pilot_color, pilot_time=Utils.get_str_lap_time_from_lap(lap)))
        fig = self.__set_labels(fig)
        plt.suptitle('Basic Telemtry Data\n' + lap_name)
        fig = self.__plot_sectors(fig, lap)
        plt.show()
        self.__pilot_patch = []
        return
    
    def plot_comparison(self, laps: list[fastf1.core.Lap], pilots: list[str], lap_name: str):
        """Plot basic telemetry data (Speed, RPM, Gear, Throttle, Break) for the given pilot on the given lap

        Keyword arguments:
        laps        -- List of laps for which you want to plot telemetry data
        pilots      -- List of names of the pilots who made the corresponding laps
        lap_name    -- The name you want to give to the lap (will be in the graph title)
        """
        fig, axes = self.__init_graph()
        for i in range(0, len(pilots), 1):
            car_data = fastf1.core.Telemetry(laps[i].get_car_data().add_distance())
            pilot_color = fastf1.plotting.driver_color(pilots[i])
            fig = self.__plot_data(fig, car_data, pilot_color, pilots[i])
            fig = self.__plot_max_speed(fig, car_data, pilot_color)
            self.__pilot_patch.append(self.__get_pilot_patch(pilot=pilots[i], pilot_color=pilot_color, pilot_time=Utils.get_str_lap_time_from_lap(laps[i])))
        fig = self.__set_labels(fig)
        plt.suptitle('Basic Telemtry Data\n' + lap_name)
        fig = self.__plot_sectors(fig, laps[0])
        plt.show()
        self.__pilot_patch = []
        return

    def __plot_sectors(self, fig: plt.Figure, lap: fastf1.core.Lap):
        '''Plot sectors position for each axes on the given graph

        Keyword arguments:
        fig - The graph on which you want to plot sectors position
        lap - The lap for which you want to plot the sectors
        '''
        sectors = Utils.get_sectors_position(lap)
        for axe in fig.axes:
            axe.axvline(0, color=self.__SECTOR_COLOR, linestyle = 'dotted', alpha = self.__SECTOR_ALPHA)
            axe.axvline(sectors[0], color=self.__SECTOR_COLOR, linestyle = 'dotted', alpha = self.__SECTOR_ALPHA)
            axe.axvline(sectors[1], color=self.__SECTOR_COLOR, linestyle = 'dotted', alpha = self.__SECTOR_ALPHA)
            axe.axvline(self.__DISTANCE_MAX, color=self.__SECTOR_COLOR, linestyle = 'dotted', alpha = self.__SECTOR_ALPHA)
        y_lim = fig.axes[0].get_ylim()[1]
        fig.axes[0].text(0, y_lim, 'Sector 1', color=self.__SECTOR_COLOR, alpha = self.__SECTOR_ALPHA)
        fig.axes[0].text(sectors[0], y_lim, 'Sector 2', color=self.__SECTOR_COLOR, alpha = self.__SECTOR_ALPHA)
        fig.axes[0].text(sectors[1], y_lim, 'Sector 3', color=self.__SECTOR_COLOR, alpha = self.__SECTOR_ALPHA)
        return fig
    
    def __init_graph(self):
        """Initialize the graph grid and ratios
        """
        gridspec_kw = dict(
            # Defines the heights of the two plots 
            # (bottom plot twice the size of the top plot)
            height_ratios=(1, 1, 1, 1, 1),  
            # 0.1 space between axes
            hspace=0.1,
        )
        fig, axes = plt.subplots(
            nrows=5, ncols=1, sharex=True, gridspec_kw=gridspec_kw,
        )
        return fig, axes
    
    def __set_labels(self, fig: plt.Figure):
        """Set all the Basic Telemetry Graph labels

        Keyword arguments:
        fig -- Graph on which you want to set labels
        """
        fig.axes[4].set_xlabel('Distance [m]')
        fig.axes[0].set_ylabel('Speed [km/h]')
        fig.axes[1].set_ylabel('RPM')
        fig.axes[2].set_ylabel('Gear')
        fig.axes[3].set_ylabel('Throttle [%]')
        fig.axes[4].set_ylabel('Brake')
        fig.axes[0].legend(handles=self.__pilot_patch)
        return fig

    def __plot_data(self, fig: plt.Figure, car_data: fastf1.core.Telemetry, pilot_color: str, pilot: str):
        """Plot all the basic data for the given pilot

        Keywords arguments:
        fig         -- Graph on which you want to plot data
        car_data    -- Telemetry data of a car on one lap
        pilot_color -- Graph color of the pilot
        pilot       -- Name or label of the pilot
        """
        x = car_data['Distance']
        self.__DISTANCE_MAX = car_data['Distance'].iloc[-1]
        fig.axes[0].plot(x, car_data['Speed'], color = pilot_color, label=pilot)
        fig.axes[1].plot(x, car_data['RPM'], color = pilot_color, label=pilot)
        fig.axes[2].plot(x, car_data['nGear'], color = pilot_color, label=pilot)
        fig.axes[3].plot(x, car_data['Throttle'], color = pilot_color, label=pilot)
        fig.axes[4].plot(x, car_data['Brake'], color = pilot_color, label=pilot)
        return fig
    
    def __plot_max_speed(self, fig: plt.Figure, car_data: fastf1.core.Telemetry, pilot_color: str):
        """Plot max speed on the SPEED subplot

        Keywords arguments:
        fig         -- Graph on which you want to plot data
        car_data    -- Telemetry data of a car on one lap
        pilot_color -- Graph color of the pilot
        """
        (xmax, ymax) = self.__get_max_speed_coordinates(car_data)
        fig.axes[0].plot(xmax, ymax, marker="o", markersize=3, markeredgecolor="red", markerfacecolor=pilot_color)
        return fig

    def __get_pilot_patch(self, pilot: str, pilot_color: str, pilot_time: str):
        """Build mpatches.Patch object for the figure legend

        Keywords arguments:
        pilot       - Name of the pilot
        pilot_color - color of the pilot
        pilot_time  - pilot time (m:s:ms)
        """
        pilot_patch = mpatches.Patch(color=pilot_color, label=pilot + ' - ' + pilot_time, clip_on=False)
        return pilot_patch

    def __get_max_speed_coordinates(self, car_data: fastf1.core.Telemetry):
        """Get the max speed coordinates (max_speed, max_speed_distance)

        Keywords arguments:
        car_data    - Car data of the lap from which you want to get the max speeed coordinates by distance
        """
        max_speed = car_data['Speed'].max()
        max_speed_index = car_data['Speed'].idxmax()
        distance_for_max_speed = car_data['Distance'][max_speed_index]
        return (distance_for_max_speed, max_speed)

