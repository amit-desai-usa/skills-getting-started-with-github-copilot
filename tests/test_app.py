from fastapi.testclient import TestClient

from src.app import activities, app

client = TestClient(app)


def test_unregister_participant_removes_email():
    activity_name = "Chess Club"
    activities[activity_name]["participants"] = ["michael@mergington.edu", "daniel@mergington.edu"]

    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": "daniel@mergington.edu"},
    )

    assert response.status_code == 200
    assert "daniel@mergington.edu" not in activities[activity_name]["participants"]
    assert response.json()["message"] == "Removed daniel@mergington.edu from Chess Club"


def test_unregister_participant_missing_email_returns_404():
    activity_name = "Programming Class"
    activities[activity_name]["participants"] = ["emma@mergington.edu"]

    response = client.delete(
        f"/activities/{activity_name}/participants",
        params={"email": "not-here@mergington.edu"},
    )

    assert response.status_code == 404
    assert response.json()["detail"] == "Participant not found"
