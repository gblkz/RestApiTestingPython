"""
Test file for todo_api.py
- Uses existing API built/hosted by course instructor. Has video demoing how to build it.

Other new commit. Now what?
"""
import requests
import uuid

ENDPOINT = "https://todo.pixegami.io"
"""
response = requests.get(ENDPOINT)   # Making an HTTP Request.
print(response)                     # prints just the status code, [200].
data = response.json()              # returns the entire response message.
print(data)                         # prints the hello message.
status_code = response.status_code  # returns just the status code.
print(status_code)                  # prints just the status code.
"""


# def test_can_call_endpoint():
#     response_root = requests.get(ENDPOINT)
#     assert response_root.status_code == 200  # pass for 200, fail otherwise.


def test_can_create_task():
    # Payload has the Request body having the endpoint schema from the docs page.
    # Populate with test data. task_id required only for update as it's auto-generated.
    payload = new_task_payload()

    # Put operation, including the full path to this endpoint.
    # Payload as json object contains the request body having required schema.
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    data = create_task_response.json()
    # print(data)

    # We're not done. Pass result doesn't verify the API works.
    # Verify content, not just operation success.
    # Find the task_id from the response printed above. 'task_96895c1c1ee1452cb9e28704a75f7237'
    # Review the API docs for the get-schema.
    task_id = data["task"]["task_id"]
    get_task_response = get_task(task_id)

    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    # assert get_task_data["content"] == "other content"          # FAIL test to verify.
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]


def test_can_update_item():
    # create a task
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    # update the task using the random generated user_id
    new_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "my updated content",
        "is_done": True,
    }
    update_task_response = update_task(new_payload)
    assert update_task_response.status_code == 200

    # get and validate the changes
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == new_payload["content"]
    assert get_task_data["is_done"] == new_payload["is_done"]


def test_can_list_tasks():
    # Create N tasks
    n = 3                           # helper variable to simplify changes.
    payload = new_task_payload()    # payload move out of loop to simplify this test's assert.
    for _ in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    # List tasks and check that there are N tasks
    user_id = payload["user_id"]
    list_task_response = list_task(user_id)
    assert list_task_response.status_code == 200
    data = list_task_response.json()
    # print(data)             # to find out what the data looks like.
    tasks = data["tasks"]
    assert len(tasks) == n


def test_can_delete_task():
    # Create a task.
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    task_id = create_task_response.json()["task"]["task_id"]

    # Delete the task.
    delete_task_response = delete_task(task_id)
    assert delete_task_response.status_code == 200

    # Get the task and verify it's not found.
    get_task_response = get_task(task_id)
    # print(get_task_response.status_code)    # look at response to see status returned for missing endpoint.
    assert get_task_response.status_code == 404


# Helper functions below
def create_task(payload):
    return requests.put(ENDPOINT + "/create-task", json=payload)


def update_task(payload):
    return requests.put(ENDPOINT + "/update-task", json=payload)


def get_task(task_id):
    return requests.get(ENDPOINT + f"/get-task/{task_id}")


def list_task(user_id):
    return requests.get(ENDPOINT + f"/list-tasks/{user_id}")


def delete_task(task_id):
    return requests.delete(ENDPOINT + f"/delete-task/{task_id}")


def new_task_payload():
    user_id = f"test_user_{uuid.uuid4().hex}"
    content = f"test_content_{uuid.uuid4().hex}"
    # print(f"Creating task for user {user_id} with content {content}")     # just to see.
    return {
        "content": content,
        "user_id": user_id,
        # "task_id": "test_task_id",
        "is_done": False,
    }
