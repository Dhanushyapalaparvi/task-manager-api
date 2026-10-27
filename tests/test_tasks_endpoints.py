def test_get_tasks_returns_list(client):
    response = client.get("/tasks")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_tasks_invalid_limit(client):
    response = client.get("/tasks?limit=101")
    assert response.status_code == 422


def test_get_tasks_negative_skip(client):
    response = client.get("/tasks?skip=-1")
    assert response.status_code == 422


def test_create_task(client):
    task_data = {
        "title":"Learn FastApi testing",
        "description":"Write automated tests using pytest",
        "completed":False,
    }
    response = client.post("/tasks",json = task_data)

    assert response.status_code == 201

    data = response.json()

    assert data["id"] is not None
    assert data["title"] == "Learn FastApi testing"
    assert data["description"] == "Write automated tests using pytest"
    assert data["completed"] is False

def test_task_create_without_title(client):
    task_data = {
        "description":"This task has no title",
        "completed": False,
    }

    response = client.post("/tasks",json = task_data)

    assert response.status_code == 422

def test_get_task_by_id(client):
    create_response = client.post(
        "/tasks",
        json = {
            "title":"Practice FastApi",
            "description":"learn automated testing",
            "completed":False,
        },
    )
    task_id = create_response.json()["id"]
    response = client.get(f"/tasks/{task_id}")

    assert response.status_code == 200
    assert response.json()["id"] == task_id
    assert response.json()["title"] == "Practice FastApi"

def test_non_existent_task(client):
    response = client.get("/tasks/99999")

    assert response.status_code == 404


def test_update_task(client):
    create_response = client.post(
        "/tasks",
        json = {
            "title":"Old title",
            "description":"Old description",
            "completed":False,
        },
    )
    task_id = create_response.json()["id"]
    response = client.put(
        f"/tasks/{task_id}",
        json = {
            "title":"Updated title",
            "description":"Updated description",
            "completed":True,
        },

    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated title"
    assert response.json()["completed"] is True


def test_patch_task(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Study Python",
            "description": "Practice daily",
            "completed": False,
        },
    )

    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"completed": True},
    )

    assert response.status_code == 200
    assert response.json()["title"] == "Study Python"
    assert response.json()["completed"] is True

def test_delete_task(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Temporary task",
            "description": "Delete this task",
            "completed": False,
        },
    
    )
    task_id = create_response.json()["id"]

    response = client.delete(f"/tasks/{task_id}")

    assert response.status_code in (200,204)

    get_response = client.get(f"tasks/{task_id}")
    assert get_response.status_code == 404


def test_create_task_uses_default_priority(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Default priority task",
            "completed": False,
        },
    )
    assert response.status_code == 201
    assert response.json()["priority"] == "medium"

def test_create_task_with_custom_priority(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Urgent task",
            "completed": False,
            "priority": "high",
        },
    )
    assert response.status_code == 201
    assert response.json()["priority"] == "high"


def test_create_task_rejects_invalid_priority(client):
    response = client.post(
        "/tasks",
        json={
            "title": "Invalid priority task",
            "completed": False,
            "priority": "urgent",
        },
    )

    assert response.status_code == 422

def test_patch_priority_preserves_other_fields(client):
    create_response = client.post(
        "/tasks",
        json={
            "title": "Finish assignment",
            "description": "Complete the API project",
            "completed": False,
            "priority": "low",
        },
    )
    assert create_response.status_code == 201
    task_id = create_response.json()["id"]
    response = client.patch(
        f"/tasks/{task_id}",
        json = {"priority":"high"},
    )

    assert response.status_code == 200

    data = response.json()
    assert data["priority"] == "high"
    assert data["title"] == "Finish assignment"
    assert data["description"] == "Complete the API project"
    assert data["completed"] is False



def test_patch_task_rejects_null_completed(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Test task"},
    )
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"completed": None},
    )

    assert response.status_code == 422


def test_patch_task_rejects_null_priority(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Test task"},
    )
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"priority": None},
    )

    assert response.status_code == 422


def test_patch_task_rejects_empty_title(client):
    create_response = client.post(
        "/tasks",
        json={"title": "Test task"},
    )
    task_id = create_response.json()["id"]

    response = client.patch(
        f"/tasks/{task_id}",
        json={"title": ""},
    )

    assert response.status_code == 422
