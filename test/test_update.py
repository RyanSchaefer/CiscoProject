from src import update_object as o_obj
from mock_db import create_db
import pytest
import json

STARTING_DB_INPUT = {
    "some_uid": {
        "firstName": "Andrey",
        "lastName": "Kolmogorov",
        "dob": "25 April 1903"
    }
}
INP = json.dumps({
        "firstName": "Andrey",
        "lastName": "Kolmogorov",
        "dob": "19030425",
        "dod": "19871020"
})


def test_update():
    starting_db = create_db()
    actual: dict = o_obj.update_object_in_db(
        starting_db,
        "some_uid",
        INP
    )
    assert actual == INP


def test_update_twice_same_result():
    starting_db = create_db()
    actual: dict = o_obj.update_object_in_db(
        starting_db,
        "some_uid",
        INP
    )
    actual2: dict = o_obj.update_object_in_db(
        starting_db,
        "some_uid",
        INP
    )
    assert actual == INP == actual2


def test_no_uid_causes_error():
    empty = create_db()
    with pytest.raises(ValueError):
        o_obj.update_object_in_db(
            empty,
            "any_uid",
            INP
        )


def test_attempt_to_add_uid_key_causes_error():
    starting_db = create_db()
    with pytest.raises(ValueError):
        o_obj.handle_helper(
            starting_db,
            "some_uid",
            json.dumps({
                "uid": "I can TOTALLY update someone elses object"
            })
        )

def test_update_to_non_json():
    starting_db = create_db()
    with pytest.raises(ValueError):
        o_obj.handle_helper(
            starting_db,
            "some_uid",
            "this isn't json :("
        )
