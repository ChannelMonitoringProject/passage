# from passage.api.utils.redis_helpr import lists_to_dicts
from api.utils import redis_helper


def test_lists_to_dicts():
    l = [
        ["mmsi", 1234, "name", "aarlos"],
        ["mmsi", 1235, "name", "carlos"],
        ["mmsi", 1236, "name", "narlos"],
        ["mmsi", 1237, "name", "darlos"],
    ]
    dicts = redis_helper.lists_to_dicts(l)
    assert dicts == [
        {
            "mmsi": 1234,
            "name": "aarlos",
        },
        {
            "mmsi": 1235,
            "name": "carlos",
        },
        {
            "mmsi": 1236,
            "name": "narlos",
        },
        {
            "mmsi": 1237,
            "name": "darlos",
        },
    ]
