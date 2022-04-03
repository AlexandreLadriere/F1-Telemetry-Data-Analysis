from tabnanny import check
import matplotlib.pyplot as plt
import fastf1.plotting


SESSION_DICT = {'FP1' : 'Practice 1', 'FP2' : 'Practice 2', 'FP3' : 'Practice 3', 'Q' : 'Qualifying', 'SQ' : 'Sprint Qualifying', 'R' : 'Race'}
CACHE_DIRECTORY = 'doc_cache'
YEAR = 2022
WEEKEND = 2 # Can be number, name, ...
PILOTS = ['VER', 'LEC']
SESSION = 'q'

#Check if session qualifier exists
def check_if_session_identifier_is_valid(dict, identifier):
    identifier = identifier.upper()
    for session in dict:
        if (session.upper() == identifier or dict[session].upper() == identifier):
            return True
    return False

# Setup color scheme and cache directory
def setup(cache_directory):
    fastf1.Cache.enable_cache(cache_directory)
    # enable some matplotlib patches for plotting timedelta values and load
    # FastF1's default color scheme
    fastf1.plotting.setup_mpl()

# Load specified event if it exists or raise an error otherwise
def load_event(year, weekend):
    # load a session and its telemetry data
    try:
        event = fastf1.get_event(year, weekend)
        return event
    except:
        raise Exception("The 'year' or the 'weekend' is incorrect or does not exists")

# Load specified session if it exists or raise an error otherwise
def load_session(event, session_identifier):
    if check_if_session_identifier_is_valid(SESSION_DICT, session_identifier) != True:
        raise Exception("The session identifier is invalid")
    else:
        try:
            session = event.get_session(session_identifier)
            session.load()
            return session
        except:
            raise Exception("The session could not be loaded")

# Check if specified pilots (must be a list) exists in the specified session
def check_if_pilot_exists_in_session(session, pilot):
    for abr in session.results['Abbreviation']:
        if pilot.upper() == abr.upper():
            return True
    return False

# Get fastest lap for specified session and pilot (must be a list)
def get_pilots_fastest_lap(session, pilots):
    fastest_laps = []
    for pilot in pilots:
        if (check_if_pilot_exists_in_session(session, pilot) == True):
            fastest_laps.append(session.laps.pick_driver(pilot.upper()).pick_fastest())
        else:
            raise Exception("One of the input pilot does not exist")
    return fastest_laps

# Get lap telemetry for specified laps(must be a list)
def get_pilots_telemetry(laps):
    laps_tel = []
    for lap in laps:
        laps_tel.append(lap.get_car_data().add_distance())
    return laps_tel

# Get specific pilot color for specified laps(must be a list)
def get_pilots_color(laps):
    colors = []
    for lap in laps:
        colors.append(fastf1.plotting.team_color(lap['Team']))
    return colors


def plot_speed_by_distance(laps_telemetry, pilots_color, pilots, ax):
    for i in range(len(pilots)):
        ax.plot(laps_telemetry[i]['Distance'], laps_telemetry[i]['Speed'], color=pilots_color[i], label=pilots[i])
    ax.set_xlabel('Distance in m')
    ax.set_ylabel('Speed in km/h')
    ax.legend()

def plot_brake_pedal_pressure(laps_telemetry, pilots_color, pilots, ax):
    for i in range(len(pilots)):
        ax.plot(laps_telemetry[i]['Distance'], laps_telemetry[i]['Brake'], color=pilots_color[i], label=pilots[i])
    ax.set_ylabel('Brake pedal pressure')
    ax.legend()
    ax.set_xlabel('Distance in m')


setup(CACHE_DIRECTORY)
event = load_event(YEAR, WEEKEND)
session = load_session(event, SESSION)
pilots_fastest_lap = get_pilots_fastest_lap(session, PILOTS)
pilots_fastest_lap_tel = get_pilots_telemetry(pilots_fastest_lap)
pilots_color = get_pilots_color(pilots_fastest_lap)
fig, (ax1, ax2) = plt.subplots(2)
plot_speed_by_distance(pilots_fastest_lap_tel, pilots_color, PILOTS, ax1)
plot_brake_pedal_pressure(pilots_fastest_lap_tel, pilots_color, PILOTS, ax2)
plt.suptitle(f"Fastest Lap Comparison \n "
            f"{session.event['EventName']} {session.event.year} Qualifying")
plt.show()