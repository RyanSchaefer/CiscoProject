import pytest
from src import get_object as g_obj
from mock_db import MockDatabase
import json

STARTING_DB_INPUT = {
    "some_uid": {
        "firstName": "Andrey",
        "lastName": "Kolmogorov",
        "dob": "25 April 1903"
    }
}

BASE_URL = "https://myapp.com/api"


def test_get_one_valid_obj():
    db = MockDatabase(STARTING_DB_INPUT)
    actual: dict = g_obj.handle_helper(db, "some_uid")
    expected = STARTING_DB_INPUT["some_uid"]
    expected["uid"] = "some_uid"
    assert actual == expected


def test_get_all_valid_objs():
    db = MockDatabase(STARTING_DB_INPUT)
    db.put_item(item={
        "uid": "another_uid",
        "data": "something"
    })
    actual = g_obj.handle_helper(db)
    assert set(json.loads(actual)) == {
        f"{BASE_URL}/api/objects/another_uid",
        f"{BASE_URL}/api/objects/some_uid"
    }


def test_get_invalid_obj():
    db = MockDatabase()
    with pytest.raises(ValueError):
        g_obj.handle_helper(
            db,
            "bad uid"
        )
