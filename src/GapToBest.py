import fastf1
import fastf1.plotting
import Utils
from timple.timedelta import strftimedelta


from matplotlib import pyplot as plt

fastf1.plotting.setup_mpl()

class GapToBest:

    __COLOR_Q1_107_TIME = 'y'
    __ALPHA_Q1_107_TIME = 0.8
    __COLUMN_LAP_TIME = 'LapTime'
    __COLUMN_LAP_TIME_DELTA = 'LapTimeDelta'
    __LABEL_X_AXE = 'Gap to Best (s)'
    __FORMAT_TIME = '%m:%s.%ms'
    __PADDING_BAR_LABEL = 5
    __FORMAT_BAR_LABEL = '+%g s'

    def plot(self, session: fastf1.core.Session, qualifying = True):
        session.load()
        #Get fastest lap for each driver and sort them
        drivers_fastest_laps = Utils.get_fastest_laps(session)
        drivers_fastest_laps = fastf1.core.Laps(drivers_fastest_laps).sort_values(by=self.__COLUMN_LAP_TIME).reset_index(drop=True)
        #Get fastest lap of all and add difference to it for others
        pole_lap = drivers_fastest_laps.pick_fastest()
        drivers_fastest_laps[self.__COLUMN_LAP_TIME_DELTA] = drivers_fastest_laps[self.__COLUMN_LAP_TIME] - pole_lap[self.__COLUMN_LAP_TIME]
        #Get 107% time
        if (qualifying):
            Q1_107_time = Utils.get107Time(session)
            Q1_107_time_diff = Q1_107_time - pole_lap[self.__COLUMN_LAP_TIME]
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
        bar_labels = []
        for index, row in drivers_fastest_laps.iterrows():
            yticklabels.append(row['Driver'] + ' (' + Utils.DICT_COMPOUND[row['Compound']] + ')')
            x_values.append(row[self.__COLUMN_LAP_TIME_DELTA].total_seconds())
            bar_labels.append(str(strftimedelta(row[self.__COLUMN_LAP_TIME], self.__FORMAT_TIME)))
        #plot hbar
        bars = ax.barh(drivers_fastest_laps.index, x_values,
                color=team_colors, edgecolor='grey')
        ax.bar_label(bars, padding=self.__PADDING_BAR_LABEL, fmt=self.__FORMAT_BAR_LABEL)
        #plot 107% time diff
        if (qualifying):
            ax.axvline(Q1_107_time_diff.total_seconds(), color=self.__COLOR_Q1_107_TIME, linestyle = 'dotted', alpha = self.__ALPHA_Q1_107_TIME)
            ax.text(Q1_107_time_diff.total_seconds() + 0.1, 0, 'Q1 107% time - ' + str(strftimedelta(Q1_107_time, self.__FORMAT_TIME)) + ' s', alpha = self.__ALPHA_Q1_107_TIME, color=self.__COLOR_Q1_107_TIME)
        #Build yticks and yticklabels
        ax.set_yticks(drivers_fastest_laps.index)
        ax.set_yticklabels(yticklabels)
        # show fastest at the top
        ax.invert_yaxis()
        # draw vertical lines behind the bars
        ax.set_axisbelow(True)
        ax.xaxis.grid(True, which='major', linestyle='--', color='black', zorder=-1000)
        plt.xlabel(self.__LABEL_X_AXE)
        lap_time_string = strftimedelta(pole_lap[self.__COLUMN_LAP_TIME], self.__FORMAT_TIME)
        plt.suptitle(f"{session.event['EventName']} {session.event.year} Qualifying\n"
                    f"Fastest Lap: {lap_time_string} ({pole_lap['Driver']})")
        plt.show()
        return