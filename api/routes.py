from flask import Blueprint, jsonify
import redis, json
from .plotter import generate_ais_plot

bp = Blueprint("api", __name__)
r = redis.Redis(host="localhost", port=6379, db=0)


@bp.route("/ais/latest-plot")
def latest_plot():
    raw_msgs = r.lrange("ais:latest", 0, 99)  # last 100
    data = [json.loads(m) for m in raw_msgs]

    fig = generate_plot(data)
    return jsonify(fig)
