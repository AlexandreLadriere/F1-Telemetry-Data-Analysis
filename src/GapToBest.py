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
        Q1_107_time = Utils.get107Time(session)
        Q1_107_time_diff = Q1_107_time - pole_lap['LapTime']
        print(Q1_107_time_diff.total_seconds())
        #Get team colors
        team_colors = list()
        for index, lap in drivers_fastest_laps.iterlaps():
            color = fastf1.plotting.team_color(lap['Team'])
            team_colors.append(color)
        #plot fig
        fig, ax = plt.subplots()
        #build x axes values and y tick labels
        yticklabels = []
        x_values = []
        for index, row in drivers_fastest_laps.iterrows():
            yticklabels.append(row['Driver'] + ' (' + Utils.DICT_COMPOUND[row['Compound']] + ')')
            x_values.append(row['LapTimeDelta'].total_seconds())
        #plot hbar
        ax.barh(drivers_fastest_laps.index, x_values,
                color=team_colors, edgecolor='grey')
        ax.set_yticks(drivers_fastest_laps.index)
        #plot 107% time diff
        ax.axvline(Q1_107_time_diff.total_seconds(), color='y', linestyle = 'dotted', alpha = 0.8)
        #Build yticklabels and x axes values
        ax.set_yticklabels(yticklabels)
        # show fastest at the top
        ax.invert_yaxis()
        # draw vertical lines behind the bars
        ax.set_axisbelow(True)
        ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)
        plt.xlabel('Gap to Best (s)')
        ax.text(Q1_107_time_diff.total_seconds() + 0.1, 0, 'Q1 107% time - ' + str(strftimedelta(Q1_107_time, '%m:%s.%ms')), alpha = 0.8, color='y')
        lap_time_string = strftimedelta(pole_lap['LapTime'], '%m:%s.%ms')
        plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\n"
                    f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")
        plt.show()
        return