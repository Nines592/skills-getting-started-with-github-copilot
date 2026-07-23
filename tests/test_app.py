from copy import deepcopy
from urllib.parse import quote

import pytest
from fastapi.testclient import TestClient

from src import app as app_module


@pytest.fixture(autouse=True)
def reset_activities():
    original = deepcopy(app_module.activities)
    yield
    app_module.activities.clear()
    app_module.activities.update(original)


def test_unregister_participant_removes_them_from_activity():
    client = TestClient(app_module.app)
    email = "michael@mergington.edu"

    response = client.delete(
        f"/activities/Chess Club/participants/{quote(email, safe='')}"
    )

    assert response.status_code == 200
    assert response.json()["message"] == f"Removed {email} from Chess Club"

    activities = client.get("/activities").json()
    assert email not in activities["Chess Club"]["participants"]
