from src import create_object as c_obj
from mock_db import MockDatabase
import pytest
import json

INP = json.dumps({
        "firstName": "Andrey",
        "lastName": "Kolmogorov",
        "dob": "25 April 1903"
    })

def test_single_create():

    actual: dict = c_obj.handle_helper(MockDatabase(), INP)
    assert actual.get("uid", False)
    # remove uid to check if object is still the same
    del actual["uid"]
    assert actual == INP


def test_multi_create():
    db = MockDatabase()
    actual: dict = c_obj.handle_helper(db, INP)
    actual2: dict = c_obj.handle_helper(db, INP)
    assert actual["uid"] != actual2["uid"]
    del actual["uid"]
    del actual2["uid"]
    assert actual == actual2


def test_uid_key_forbidden():
    inp = json.dumps({
        "uid": "test"
    })
    with pytest.raises(ValueError):
        c_obj.handle_helper(MockDatabase(), inp)


def test_bad_json_forbidden():
    inp = "this is some very bad json"

    with pytest.raises(ValueError):
        c_obj.handle_helper(MockDatabase(), inp)
