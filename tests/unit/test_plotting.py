from api import plotter


def test_positions_plot():
    plotter.get_state_trace()


def test_get_trace():
    plot_data = {
        "lat": [],
        "lon": [],
        "name": [],
    }
    trace = plotter.get_state_trace(plot_data)
    assert trace == []
    assert False


def test_color_boats(mocker):
    # mocker.patch("api.plotter.uk_borderforce_boats", return_value=["boaty"])
    mocker.patch("api.plotter.uk_borderforce_boats", ["boaty"])
    mocker.patch("api.plotter.french_navy_boats", ["mcboatface"])
    boats = [{"name": "boaty"}, {"name": "mcboatface"}]
    plotter.color_boats(boats)
    assert boats[0]["color"] == "red"
    assert boats[1]["color"] == "blue"
