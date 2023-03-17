import fastf1
import fastf1.plotting
import typing

from matplotlib import pyplot as plt
fastf1.plotting.setup_mpl()

class BasicTelemetry:
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

        fig = self.__set_labels(fig)
        plt.suptitle('Basic Telemtry Data\n' + lap_name)
        plt.show()
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
        fig = self.__set_labels(fig)
        plt.suptitle('Basic Telemtry Data\n' + lap_name)
        plt.show()
        return
    
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
        fig.axes[0].plot(x, car_data['Speed'], color = pilot_color, label=pilot)
        fig.axes[1].plot(x, car_data['RPM'], color = pilot_color, label=pilot)
        fig.axes[2].plot(x, car_data['nGear'], color = pilot_color, label=pilot)
        fig.axes[3].plot(x, car_data['Throttle'], color = pilot_color, label=pilot)
        fig.axes[4].plot(x, car_data['Brake'], color = pilot_color, label=pilot)
        fig.axes[0].legend()
        return fig

