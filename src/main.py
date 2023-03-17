import fastf1
import fastf1.plotting
from BasicTelemetry import BasicTelemetry

fastf1.Cache.enable_cache('./cache')

session = fastf1.get_session(2019, 'Monza', 'Q')
session.load()
fast_leclerc = session.laps.pick_driver('LEC').pick_fastest()
fast_verstappen = session.laps.pick_driver('VER').pick_fastest()
fast_hamilton = session.laps.pick_driver('HAM').pick_fastest()
fast_sainz = session.laps.pick_driver('SAI').pick_fastest()
# need to plot sector limit and all turns

BT = BasicTelemetry()
#BT.plot(lap=fast_leclerc, pilot='LEC', lap_name=session.event['EventName'] + ' - ' + str(session.event.year) + ' - ' + 'Qualifying')
BT.plot_comparison(laps=[fast_leclerc, fast_sainz], pilots=['LEC', 'SAI'], lap_name=session.event['EventName'] + ' - ' + str(session.event.year) + ' - ' + 'Qualifying')
