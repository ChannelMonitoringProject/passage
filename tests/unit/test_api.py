from api import create_app


def test_get_ais_state():
    app = create_app()
    app.config.update({"TESTING": True})
    client = app.test_client()
    resp = client.get("/api/graphs/boats")
    print(resp.json)
    assert resp == None
    pass
