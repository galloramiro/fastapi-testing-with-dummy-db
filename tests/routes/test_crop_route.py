from src.schemas import CropRequest


def test_crop_route_save(setup_database, not_logged_client):
    json = CropRequest(name="Test Crop", type="Test type").dict()

    response = not_logged_client.post("/crop", json=json)

    assert response.status_code == 200
    assert response.json()["name"] == json["name"]
    assert response.json()["type"] == json["type"]


def test_crop_route_get_all(setup_database, not_logged_client):
    json = CropRequest(name="Test Crop", type="Test type").dict()
    not_logged_client.post("/crop", json=json)

    response = not_logged_client.get("/crop")

    assert response.status_code == 200
    assert len(response.json()) == 1
