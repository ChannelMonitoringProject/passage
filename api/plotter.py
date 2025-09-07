import os
import json
from collections import defaultdict
import plotly.graph_objects as go
import redis
import logging
from .utils import redis_helper


REDIS_HOST = os.environ.get("REDIS_HOST", "localhost")
REDIS_PORT = int(os.environ.get("REDIS_PORT", 6379))
REDIS_DB = int(os.environ.get("REDIS_DB", 0))
REDIS_BOAT_POSITION_REPORT_TOPIC = os.environ.get(
    "REDIS_BOAT_POSITION_REPORT_TOPIC", "ais.updates.boat_position_reports"
)
AIS_STREAM_ARENA = os.environ.get(
    "AIS_STREAM_ARENA", "[[[51.385, 0.909], [50.678, 2.667]]]"
)

redis_client = redis.Redis(host=REDIS_HOST, port=REDIS_PORT, db=REDIS_DB)


def get_arena():
    """
    Convert arena as defined in AIS_STREAM_ARENA to the one used by plot
    """
    arena = json.loads(AIS_STREAM_ARENA)
    arena_bounds = {
        "east": arena[0][0][1],
        "west": arena[0][1][1],
        "south": arena[0][1][0],
        "north": arena[0][0][0],
    }
    return arena_bounds


def get_center(arena_bounds):
    """
    get center point of areana_bouns

    :param arena_bounds [TODO:type]: [TODO:description]
    """

    center = {
        "lat": (arena_bounds["north"] + arena_bounds["south"]) / 2,
        "lon": (arena_bounds["west"] + arena_bounds["east"]) / 2,
    }
    return center


def get_state():
    """
    Get all state elements from redis
    """
    ret = []
    print(redis_client.keys())

    # state = redis_helper.get_ais_state()
    state = redis_client.scan_iter("ais.updates.boat_position_reports:*")
    for state_entry_key in state:
        state_entry = redis_client.json().get(state_entry_key)
        ret.append(state_entry)
    return ret


def get_state_boat_position_reports():
    """
    Get BoatPositionReports from redis state
    """
    ret = []
    state = redis_client.scan_iter(REDIS_BOAT_POSITION_REPORT_TOPIC + ":*")
    print(state)
    for position_report_key in state:
        print(position_report_key)
        position_report = redis_client.json().get(position_report_key)
        ret.append(position_report)
    return ret


def to_defaultdict(list_of_dicts):
    """
    helper to convert from list of dicts [{"mmsi":123, ...}, ... ]
    to a dict of lists { "mmsi": [123, ...], "ship_name":["boaty", ...], ... }

    :param list_of_dicts
    """
    ret = defaultdict(list)
    for d in list_of_dicts:
        for k, v in d.items():
            ret[k].append(v)
    return ret


def get_state_trace():
    boat_position_reports = get_state_boat_position_reports()
    plot_data = to_defaultdict(boat_position_reports)
    ret = go.Scattermapbox(
        name="state_trace",
        lat=plot_data["lat"],
        lon=plot_data["lon"],
        mode="markers+text",
        marker=dict(
            size=12,
        ),
        text=plot_data["ship_name"],
        textposition="top right",
        showlegend=False,
    )
    return ret


def plot_state():
    arena = get_arena()
    center = get_center(arena)
    zoom = 10

    state_trace = get_state_trace()

    fig = go.Figure()
    fig.add_trace(state_trace)

    fig.update_layout(
        mapbox=dict(
            style="open-street-map",  # Use OpenStreetMap as the background
            center=dict(
                lat=center["lat"],
                lon=center["lon"],
            ),
            zoom=zoom,
        ),
        margin={"r": 0, "t": 0, "l": 0, "b": 0},
    )
    return fig
