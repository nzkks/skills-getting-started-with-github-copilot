"""
Test suite for the Mergington High School API
Following AAA (Arrange-Act-Assert) testing pattern
"""

import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)


class TestActivities:
    """Tests for activity endpoints"""

    def test_get_activities(self):
        """Test retrieving all activities"""
        # Arrange - No special setup needed
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, dict)
        assert "Chess Club" in data
        assert "Programming Class" in data

    def test_get_activities_has_required_fields(self):
        """Test that activities have required fields"""
        # Arrange - No special setup needed
        
        # Act
        response = client.get("/activities")
        
        # Assert
        assert response.status_code == 200
        activities = response.json()
        
        for activity_name, activity_data in activities.items():
            assert "description" in activity_data
            assert "schedule" in activity_data
            assert "max_participants" in activity_data
            assert "participants" in activity_data


class TestSignup:
    """Tests for signup endpoints"""

    def test_signup_for_activity_success(self):
        """Test successful signup for an activity"""
        # Arrange
        email = "newstudent@mergington.edu"
        activity_name = "Chess Club"
        
        # Act
        response = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        data = response.json()
        assert "Signed up" in data["message"]
        assert email in data["message"]

    def test_signup_activity_not_found(self):
        """Test signup for non-existent activity"""
        # Arrange
        email = "student@mergington.edu"
        nonexistent_activity = "Nonexistent Club"
        
        # Act
        response = client.post(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]

    def test_signup_duplicate_student(self):
        """Test that duplicate signups are prevented"""
        # Arrange
        email = "duplicate@mergington.edu"
        activity_name = "Chess Club"
        
        # Act - First signup (should succeed)
        response1 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert first signup
        assert response1.status_code == 200
        
        # Act - Second signup (should fail)
        response2 = client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert second signup fails
        assert response2.status_code == 400
        assert "already signed up" in response2.json()["detail"]


class TestRemoveSignup:
    """Tests for removing signup"""

    def test_remove_signup_success(self):
        """Test successful removal from activity"""
        # Arrange
        email = "removal@mergington.edu"
        activity_name = "Chess Club"
        
        # First signup the student
        client.post(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Act - Remove the signup
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 200
        assert "Removed" in response.json()["message"]

    def test_remove_signup_not_signed_up(self):
        """Test removal when student is not signed up"""
        # Arrange
        email = "notsignedup@mergington.edu"
        activity_name = "Chess Club"
        
        # Act
        response = client.delete(
            f"/activities/{activity_name}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 400
        assert "not signed up" in response.json()["detail"]

    def test_remove_signup_activity_not_found(self):
        """Test removal from non-existent activity"""
        # Arrange
        email = "student@mergington.edu"
        nonexistent_activity = "Nonexistent Club"
        
        # Act
        response = client.delete(
            f"/activities/{nonexistent_activity}/signup",
            params={"email": email}
        )
        
        # Assert
        assert response.status_code == 404
        assert "Activity not found" in response.json()["detail"]


class TestRoot:
    """Tests for root endpoint"""

    def test_root_redirect(self):
        """Test that root redirects to static index.html"""
        # Arrange - No special setup needed
        
        # Act
        response = client.get("/", follow_redirects=False)
        
        # Assert
        assert response.status_code == 307
        assert response.headers["location"] == "/static/index.html"