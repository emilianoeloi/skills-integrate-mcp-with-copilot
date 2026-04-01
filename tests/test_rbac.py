from fastapi.testclient import TestClient

from src.app import app


client = TestClient(app)


def test_student_can_list_activities():
    response = client.get("/activities", headers={"X-User-Role": "student"})
    assert response.status_code == 200


def test_student_can_signup_and_unregister():
    email = "rbac.student@mergington.edu"

    signup = client.post(
        "/activities/Chess%20Club/signup",
        params={"email": email},
        headers={"X-User-Role": "student"},
    )
    assert signup.status_code == 200

    unregister = client.delete(
        "/activities/Chess%20Club/unregister",
        params={"email": email},
        headers={"X-User-Role": "student"},
    )
    assert unregister.status_code == 200


def test_student_cannot_create_activity():
    response = client.post(
        "/activities",
        json={
            "name": "Science Club",
            "description": "Experiments and STEM projects",
            "schedule": "Mondays, 3:30 PM - 4:30 PM",
            "max_participants": 12,
        },
        headers={"X-User-Role": "student"},
    )
    assert response.status_code == 403


def test_organizer_can_create_and_update_activity():
    create_response = client.post(
        "/activities",
        json={
            "name": "Organizer Club",
            "description": "Club created by organizer",
            "schedule": "Tuesdays, 3:30 PM - 4:30 PM",
            "max_participants": 10,
        },
        headers={"X-User-Role": "organizer"},
    )
    assert create_response.status_code == 200

    update_response = client.patch(
        "/activities/Organizer Club",
        json={"max_participants": 14},
        headers={"X-User-Role": "organizer"},
    )
    assert update_response.status_code == 200


def test_admin_can_delete_activity():
    create_response = client.post(
        "/activities",
        json={
            "name": "Admin Delete Club",
            "description": "Temporary activity for delete validation",
            "schedule": "Fridays, 3:30 PM - 4:30 PM",
            "max_participants": 8,
        },
        headers={"X-User-Role": "admin"},
    )
    assert create_response.status_code == 200

    delete_response = client.delete(
        "/activities/Admin Delete Club",
        headers={"X-User-Role": "admin"},
    )
    assert delete_response.status_code == 200


def test_invalid_role_returns_401():
    response = client.post(
        "/activities",
        json={
            "name": "Invalid Role Club",
            "description": "Should fail",
            "schedule": "Wednesdays, 3:30 PM - 4:30 PM",
            "max_participants": 10,
        },
        headers={"X-User-Role": "teacher"},
    )
    assert response.status_code == 401
