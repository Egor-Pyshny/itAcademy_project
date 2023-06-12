from httpx import Client, get

base_url = "http://localhost:8000/bbsh_api"


def test_lesson04_happy_test() -> None:
    resp = get(f"{base_url}/menu/")
    assert resp.status_code == 200
