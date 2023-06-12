from httpx import get

base_url = "http://localhost:8000/bbsh_api"


def test_health() -> None:
    resp = get(f"{base_url}/menu/")
    assert resp.status_code == 200
