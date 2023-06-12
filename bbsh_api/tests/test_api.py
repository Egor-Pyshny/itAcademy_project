import json
import uuid

from httpx import get, Client

base_url = "http://localhost:8000/bbsh_api"


def test_health():
    with Client() as client:
        resp = client.get(url=f"{base_url}/menu/")
    assert resp.status_code == 200


def check_uuid(uuid_str):
    try:
        uuid.UUID(uuid_str)
        return True
    except ValueError:
        return False


def test_user():
    with Client() as client:
        data = {
            "username": "testuser",
            "password": "testpassword",
            "phone": "00000000"
        }
        resp = client.put(url=f"{base_url}/registration/", json=data)
        uuid_str = resp.content.decode().replace('"', "")
        assert check_uuid(uuid_str)
        assert resp.status_code == 201
        resp = client.get(url=f"{base_url}/{uuid_str}/profile/")
        predicted_resp = json.dumps({
            "username": "testuser",
            "phone": "00000000",
            "id": uuid_str,
            "total orders": 0
        })
        assert predicted_resp in resp.text
        assert resp.status_code == 200
        resp = client.get(url=f"{base_url}/{uuid_str}/basket/")
        assert "[]" in resp.text
        assert resp.status_code == 200
        resp = client.get(url=f"{base_url}/{uuid_str}/history/")
        assert "[]" in resp.text
        assert resp.status_code == 200
        data = {
            "dish_name": "testposition",
            "dop_ingredients": []
        }
        resp = client.put(url=f"{base_url}/{uuid_str}/basket/add/", json=data)
        assert "true" in resp.text
        assert resp.status_code == 200
        resp = client.get(url=f"{base_url}/{uuid_str}/basket/")
        resp_data = json.loads(resp.text)
        dish_id = resp_data[0]["id"]
        predicted_resp = json.dumps(
            [
                {
                    "name": "testposition",
                    "cost": 0,
                    "size": "small",
                    "dop_ingredients": "[]",
                    "id": dish_id,
                    "user_id": uuid_str
                }
            ]
        )
        assert predicted_resp in resp.text
        assert resp.status_code == 200
        # data = json.dumps({
        #     "order_id": dish_id
        # })
        # resp = client.delete(url=f"{base_url}/{uuid_str}/basket/delete/")
        # assert "true" in resp.text
        # assert resp.status_code == 200
        resp = client.delete(url=f"{base_url}/{uuid_str}/profile/delete/")
        assert "true" in resp.text
        assert resp.status_code == 200
