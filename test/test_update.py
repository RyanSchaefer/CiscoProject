from src import update_object as o_obj
from mock_db import create_db
import pytest
import json
import moto

STARTING_DB_INPUT = [
    {
        "uid": "some_uid",
        "firstName": "Andrey",
        "lastName": "Kolmogorov",
        "dob": "25 April 1903"
    }
]
EXPECTED = {
        "uid": "some_uid",
        "firstName": "Andrey",
        "lastName": "Kolmogorov",
        "dob": "19030425",
        "dod": "19871020"
}
INP = json.dumps({
        "uid": "some_uid",
        "firstName": "Andrey",
        "lastName": "Kolmogorov",
        "dob": "19030425",
        "dod": "19871020"
})


@moto.mock_dynamodb2
def test_update():
    """
    A simple update
    """
    starting_db = create_db(STARTING_DB_INPUT)
    actual: dict = o_obj.update_object_in_db(
        starting_db,
        "some_uid",
        INP
    )
    assert actual == EXPECTED


@moto.mock_dynamodb2
def test_update_twice_same_result():
    """
    Updating twice should produce the same result
    """
    starting_db = create_db(STARTING_DB_INPUT)
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
    assert actual == EXPECTED == actual2


@moto.mock_dynamodb2
def test_no_uid_causes_error():
    """
    If the UID doesn't exist in the DB, we should return an error so people can't arbitrarily generate UIDs
    This could break idempotence but I would ask clarifying questions
    """
    empty = create_db()
    with pytest.raises(ValueError):
        o_obj.update_object_in_db(
            empty,
            "some_uid",
            INP
        )


@moto.mock_dynamodb2
def test_attempt_to_add_uid_key_causes_error():
    """
    Don't allow UIDs to be updated to different values because it could interfere with others objects
    """
    starting_db = create_db(STARTING_DB_INPUT)
    starting_db.put_item(
        Item={
            "uid": "I can TOTALLY update someone else's object"
        }
    )
    with pytest.raises(ValueError):
        o_obj.update_object_in_db(
            starting_db,
            "some_uid",
            json.dumps({
                "uid": "I can TOTALLY update someone else's object"
            })
        )


@moto.mock_dynamodb2
def test_update_to_non_json():
    """
    Don't explicitly require a uid because we can get that from the URL
    """
    starting_db = create_db(STARTING_DB_INPUT)
    with pytest.raises(ValueError):
        o_obj.update_object_in_db(
            starting_db,
            "some_uid",
            "this isn't json :("
        )


@moto.mock_dynamodb2
def test_allow_relaxed_update():
    """
    Since we can gather which UID should be updated from the URL, we should relax the object required
    to not include a UID
    """
    starting_db = create_db(STARTING_DB_INPUT)
    response = o_obj.update_object_in_db(
        starting_db,
        "some_uid",
        json.dumps({
            "my_key": "I don't include a uid, but passed it in the url"
        }))
    assert response == {
            "uid": "some_uid",
            "my_key": "I don't include a uid, but passed it in the url"
        }