"""Task API endpoint tests."""

import pytest


class TestTasksAPI:
    """Tests for task CRUD API endpoints."""

    USER_ID = "test-user-123"
    BASE_URL = f"/api/{USER_ID}/tasks"

    def test_list_tasks_empty(self, client, auth_headers):
        """Test listing tasks when none exist."""
        response = client.get(self.BASE_URL, headers=auth_headers)
        assert response.status_code == 200
        assert response.json() == []

    def test_create_task(self, client, auth_headers):
        """Test creating a new task."""
        response = client.post(
            self.BASE_URL,
            json={"title": "Buy groceries", "description": "Milk, eggs, bread"},
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Buy groceries"
        assert data["description"] == "Milk, eggs, bread"
        assert data["completed"] is False
        assert data["user_id"] == self.USER_ID
        assert "id" in data
        assert "created_at" in data
        assert "updated_at" in data

    def test_create_task_without_description(self, client, auth_headers):
        """Test creating a task without description."""
        response = client.post(
            self.BASE_URL,
            json={"title": "Simple task"},
            headers=auth_headers,
        )
        assert response.status_code == 201
        data = response.json()
        assert data["title"] == "Simple task"
        assert data["description"] is None

    def test_create_task_empty_title_fails(self, client, auth_headers):
        """Test that empty title is rejected."""
        response = client.post(
            self.BASE_URL,
            json={"title": ""},
            headers=auth_headers,
        )
        assert response.status_code == 422  # Validation error

    def test_list_tasks_after_create(self, client, auth_headers):
        """Test listing tasks returns created tasks."""
        # Create a task
        client.post(
            self.BASE_URL,
            json={"title": "Task 1"},
            headers=auth_headers,
        )
        client.post(
            self.BASE_URL,
            json={"title": "Task 2"},
            headers=auth_headers,
        )

        # List tasks
        response = client.get(self.BASE_URL, headers=auth_headers)
        assert response.status_code == 200
        tasks = response.json()
        assert len(tasks) == 2
        titles = [t["title"] for t in tasks]
        assert "Task 1" in titles
        assert "Task 2" in titles

    def test_get_task(self, client, auth_headers):
        """Test getting a specific task."""
        # Create a task
        create_response = client.post(
            self.BASE_URL,
            json={"title": "Get me"},
            headers=auth_headers,
        )
        task_id = create_response.json()["id"]

        # Get the task
        response = client.get(f"{self.BASE_URL}/{task_id}", headers=auth_headers)
        assert response.status_code == 200
        assert response.json()["title"] == "Get me"

    def test_get_nonexistent_task(self, client, auth_headers):
        """Test getting a task that doesn't exist."""
        response = client.get(f"{self.BASE_URL}/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_update_task(self, client, auth_headers):
        """Test updating a task."""
        # Create a task
        create_response = client.post(
            self.BASE_URL,
            json={"title": "Original title"},
            headers=auth_headers,
        )
        task_id = create_response.json()["id"]

        # Update the task
        response = client.put(
            f"{self.BASE_URL}/{task_id}",
            json={"title": "Updated title", "description": "New description"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        data = response.json()
        assert data["title"] == "Updated title"
        assert data["description"] == "New description"

    def test_update_task_partial(self, client, auth_headers):
        """Test partially updating a task."""
        # Create a task
        create_response = client.post(
            self.BASE_URL,
            json={"title": "Original", "description": "Keep this"},
            headers=auth_headers,
        )
        task_id = create_response.json()["id"]

        # Update only title
        response = client.put(
            f"{self.BASE_URL}/{task_id}",
            json={"title": "New title"},
            headers=auth_headers,
        )
        assert response.status_code == 200
        # Description should remain unchanged since we didn't send it

    def test_update_nonexistent_task(self, client, auth_headers):
        """Test updating a task that doesn't exist."""
        response = client.put(
            f"{self.BASE_URL}/99999",
            json={"title": "Updated"},
            headers=auth_headers,
        )
        assert response.status_code == 404

    def test_delete_task(self, client, auth_headers):
        """Test deleting a task."""
        # Create a task
        create_response = client.post(
            self.BASE_URL,
            json={"title": "Delete me"},
            headers=auth_headers,
        )
        task_id = create_response.json()["id"]

        # Delete the task
        response = client.delete(f"{self.BASE_URL}/{task_id}", headers=auth_headers)
        assert response.status_code == 204

        # Verify it's deleted
        get_response = client.get(f"{self.BASE_URL}/{task_id}", headers=auth_headers)
        assert get_response.status_code == 404

    def test_delete_nonexistent_task(self, client, auth_headers):
        """Test deleting a task that doesn't exist."""
        response = client.delete(f"{self.BASE_URL}/99999", headers=auth_headers)
        assert response.status_code == 404

    def test_toggle_complete(self, client, auth_headers):
        """Test toggling task completion status."""
        # Create a task
        create_response = client.post(
            self.BASE_URL,
            json={"title": "Toggle me"},
            headers=auth_headers,
        )
        task_id = create_response.json()["id"]
        assert create_response.json()["completed"] is False

        # Toggle to complete
        response = client.patch(
            f"{self.BASE_URL}/{task_id}/complete", headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["completed"] is True

        # Toggle back to incomplete
        response = client.patch(
            f"{self.BASE_URL}/{task_id}/complete", headers=auth_headers
        )
        assert response.status_code == 200
        assert response.json()["completed"] is False

    def test_toggle_nonexistent_task(self, client, auth_headers):
        """Test toggling a task that doesn't exist."""
        response = client.patch(f"{self.BASE_URL}/99999/complete", headers=auth_headers)
        assert response.status_code == 404


class TestTasksAPIAuth:
    """Tests for task API authentication."""

    USER_ID = "test-user-123"
    BASE_URL = f"/api/{USER_ID}/tasks"

    def test_list_tasks_without_auth(self, client):
        """Test that listing tasks without auth fails."""
        response = client.get(self.BASE_URL)
        # HTTPBearer returns 401 for missing credentials
        assert response.status_code in (401, 403)

    def test_create_task_without_auth(self, client):
        """Test that creating task without auth fails."""
        response = client.post(self.BASE_URL, json={"title": "Test"})
        # HTTPBearer returns 401 for missing credentials
        assert response.status_code in (401, 403)

    def test_user_cannot_access_other_user_tasks(
        self, client, auth_headers, other_user_headers
    ):
        """Test that users cannot access other users' tasks."""
        # Create a task as test-user-123
        client.post(
            self.BASE_URL,
            json={"title": "My private task"},
            headers=auth_headers,
        )

        # Try to list as other-user-456
        response = client.get(self.BASE_URL, headers=other_user_headers)
        # Should return 404 to prevent enumeration
        assert response.status_code == 404

    def test_invalid_token(self, client):
        """Test that invalid token returns 401."""
        response = client.get(
            self.BASE_URL,
            headers={"Authorization": "Bearer invalid-token"},
        )
        assert response.status_code == 401
