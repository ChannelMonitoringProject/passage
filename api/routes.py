from datetime import datetime, timedelta
from flask import Blueprint, jsonify, render_template
import json
from .plotter import plot_state, to_defaultdict, to_lat_lon, color_boats
from api.utils.redis_helper import get_ais_state

bp = Blueprint("api", __name__)


@bp.route("/api/")
def api_home():
    return jsonify({})


@bp.route("/api/boats/latest")
def latest(minutes=5):
    """latest state

    returns the last known position of each boat
    within the last 5 minutes
    """
    from_time = datetime.now() - timedelta(minutes=minutes)
    to_time = datetime.now()
    ret = get_ais_state(from_time.timestamp(), to_time.timestamp())
    return ret


@bp.route("api/graphs/boats")
def boats_graph():
    state = latest()
    state = to_lat_lon(state)
    color_boats(state)
    plot_data = to_defaultdict(state)
    plot = plot_state(plot_data)
    ret = json.loads(plot.to_json())
    return ret


@bp.route("/api/graphs/ais/boat_positions")
def boat_positions_graphs():
    fig = plot_state()
    fig_dict = json.loads(fig.to_json())

    # return jsonify(fig)
    return jsonify(fig_dict)
    # return fig


@bp.route("/boats")
def boats_page():
    return render_template("boats_live.html")
