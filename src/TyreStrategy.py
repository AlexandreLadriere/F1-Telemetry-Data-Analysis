import fastf1
import fastf1.plotting
import Utils
from matplotlib import pyplot as plt

fastf1.plotting.setup_mpl()

class TyreStrategy:
    def plot(self, session: fastf1.core.Session):
        """Plot tyre strategy for a session. Session must be a race (no error handling however)

        Keyword arguments:
        session -- Race for which you want to plot tyre strategy for each pilot
        """
        session.load()
        fig, ax = plt.subplots()
        driver_stints_list = []
        driver_names = []
        for driver in session.results['Abbreviation']:
            driver_laps = session.laps.pick_driver(driver)
            driver_names.append(driver_laps['Driver'].iloc[0])
            driver_stints = driver_laps[['Driver', 'Stint', 'Compound', 'LapNumber']].groupby(['Driver', 'Stint', 'Compound']).count().reset_index()
            driver_stints = driver_stints.sort_values(by=['Stint'])
            driver_stints_list.append(driver_stints)
        driver_stints_list.reverse()
        for stint in driver_stints_list:
            previous_stint_end = 0
            for index, row in stint.iterrows():
                plt.barh(row['Driver'], row['LapNumber'], left=previous_stint_end, color = Utils.DICT_COMPOUND_COLOR[row['Compound']], edgecolor = "black")
                previous_stint_end += row['LapNumber']
        plt.suptitle(f"{session.event['EventName']} {session.event.year} - Race\n"
                    f"Tyre Strategy")
        plt.xlabel('Laps')
        plt.ylabel('Drivers')
        plt.legend(handles=Utils.get_compound_patches())
        plt.show()
        return