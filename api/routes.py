from flask import Blueprint, jsonify
import redis, json
from .plotter import plot_state

bp = Blueprint("api", __name__)


@bp.route("/api/")
def api_home():
    return jsonify({})


@bp.route("/api/graphs/ais/boat_positions")
def boat_positions_graphs():
    fig = plot_state()
    fig_dict = json.loads(fig.to_json())

    # return jsonify(fig)
    return jsonify(fig_dict)
    # return fig
