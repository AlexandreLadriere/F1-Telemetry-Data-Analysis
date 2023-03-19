import fastf1
import fastf1.plotting
import numpy as np
from BasicTelemetry import BasicTelemetry

fastf1.Cache.enable_cache('./cache')

session = fastf1.get_session(2023, 'Jeddah', 'Q')
session.load()
fast_perez = session.laps.pick_driver('PER').pick_fastest()
fast_leclerc = session.laps.pick_driver('LEC').pick_fastest()
fast_gasly = session.laps.pick_driver('GAS').pick_fastest()
fast_sainz = session.laps.pick_driver('SAI').pick_fastest()
# need to plot sector limit and all turns

BT = BasicTelemetry()
#BT.plot(lap=fast_leclerc, pilot='LEC', lap_name=session.event['EventName'] + ' - ' + str(session.event.year) + ' - ' + 'Qualifying')
BT.plot_comparison(laps=[fast_perez, fast_gasly], pilots=['PER', 'GAS'], lap_name=session.event['EventName'] + ' - ' + str(session.event.year) + ' - ' + 'Qualifying')

