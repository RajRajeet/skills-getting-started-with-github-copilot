import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert len(data) > 0
    for activity in data.values():
        assert "description" in activity
        assert "participants" in activity
        assert "max_participants" in activity
        assert "schedule" in activity

def test_signup_and_unregister():
    # Pick an activity
    activities = client.get("/activities").json()
    activity_name = list(activities.keys())[0]
    email = "pytestuser@mergington.edu"

    # Sign up
    signup_url = f"/activities/{activity_name}/signup?email={email}"
    response = client.post(signup_url)
    assert response.status_code == 200
    assert "Signed up" in response.json()["message"]

    # Duplicate signup should fail
    response = client.post(signup_url)
    assert response.status_code == 400
    assert "already signed up" in response.json()["detail"]

    # Unregister
    unregister_url = f"/activities/{activity_name}/unregister?email={email}"
    response = client.post(unregister_url)
    assert response.status_code == 200
    assert "removed" in response.json()["message"]

    # Unregister again should fail
    response = client.post(unregister_url)
    assert response.status_code == 400
    assert "not registered" in response.json()["detail"]
