import fastf1
import fastf1.plotting
import Utils
from timple.timedelta import strftimedelta


from matplotlib import pyplot as plt

fastf1.plotting.setup_mpl()

class GapToBest:

    def plot(self, session: fastf1.core.Session, qualifying = True):
        session.load()
        #Get fastest lap for each driver and sort them
        drivers_fastest_laps = Utils.get_fastest_laps(session)
        print(drivers_fastest_laps)
        drivers_fastest_laps = fastf1.core.Laps(drivers_fastest_laps).sort_values(by='LapTime').reset_index(drop=True)
        #Get fastest lap of all and add difference to it for others
        pole_lap = drivers_fastest_laps.pick_fastest()
        drivers_fastest_laps['LapTimeDelta'] = drivers_fastest_laps['LapTime'] - pole_lap['LapTime']
        #Get 107% time
        
        #Get team colors
        team_colors = list()
        for index, lap in drivers_fastest_laps.iterlaps():
            color = fastf1.plotting.team_color(lap['Team'])
            team_colors.append(color)
        #plot fig
        fig, ax = plt.subplots()
        ax.barh(drivers_fastest_laps.index, drivers_fastest_laps['LapTimeDelta'],
                color=team_colors, edgecolor='grey')
        ax.set_yticks(drivers_fastest_laps.index)
        #Build yticklabels
        yticklabels = []
        for index, row in drivers_fastest_laps.iterrows():
            yticklabels.append(row['Driver'] + ' (' + Utils.DICT_COMPOUND[row['Compound']] + ')')
        ax.set_yticklabels(yticklabels)
        # show fastest at the top
        ax.invert_yaxis()
        # draw vertical lines behind the bars
        ax.set_axisbelow(True)
        ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)
        lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')
        plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\n"
                    f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")
        plt.show()
        return