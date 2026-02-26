def test_healthz(client):
    response = client.get("/healthz")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_backend_healthz(client):
    response = client.get("/backend/healthz")

    assert response.status_code == 200
    assert response.get_json() == {"status": "ok"}


def test_metrics(client):
    response = client.get("/metrics")

    assert response.status_code == 200
    assert response.mimetype == "text/plain"
    assert b"request_count" in response.data


def test_backend_metrics(client):
    response = client.get("/backend/metrics")

    assert response.status_code == 200
    assert response.mimetype == "text/plain"
    assert b"request_count" in response.data


def test_random_phrase_success(client, api_module, monkeypatch):
    monkeypatch.setattr(api_module.random, "choice", lambda _: "alpha")

    response = client.get("/random_phrase")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["phrase"] == "alpha"
    assert "selection_time" in payload
    assert isinstance(payload["selection_time"], float)


def test_backend_random_phrase_success(client, api_module, monkeypatch):
    monkeypatch.setattr(api_module.random, "choice", lambda _: "beta")

    response = client.get("/backend/random_phrase")
    payload = response.get_json()

    assert response.status_code == 200
    assert payload["phrase"] == "beta"
    assert "selection_time" in payload


def test_random_phrase_error(client, api_module, monkeypatch):
    def raise_choice_error(_):
        raise RuntimeError("forced random failure")

    monkeypatch.setattr(api_module.random, "choice", raise_choice_error)

    response = client.get("/random_phrase")
    payload = response.get_json()

    assert response.status_code == 500
    assert "error" in payload
    assert payload["error"] == "forced random failure"


def test_build_log_handler_returns_none_on_os_error(api_module, monkeypatch):
    def raise_os_error(*args, **kwargs):
        raise OSError("cannot create log dir")

    monkeypatch.setattr(api_module.os, "makedirs", raise_os_error)
    assert api_module._build_log_handler() is None
