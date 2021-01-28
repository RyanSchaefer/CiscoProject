from src import create_object as c_obj
from mock_db import create_db
import pytest
import json
import moto

INP = json.dumps({
        "firstName": "Andrey",
        "lastName": "Kolmogorov",
        "dob": "25 April 1903"
    })

@moto.mock_dynamodb2
def test_single_create():

    actual: dict = c_obj.create_object_in_db(create_db(), INP)
    assert actual.get("uid", False)
    # remove uid to check if object is still the same
    del actual["uid"]
    assert actual == json.loads(INP)

@moto.mock_dynamodb2
def test_multi_create():
    db = create_db()
    actual: dict = c_obj.create_object_in_db(db, INP)
    actual2: dict = c_obj.create_object_in_db(db, INP)
    assert actual["uid"] != actual2["uid"]
    del actual["uid"]
    del actual2["uid"]
    assert actual == actual2

@moto.mock_dynamodb2
def test_uid_key_forbidden():
    inp = json.dumps({
        "uid": "test"
    })
    with pytest.raises(ValueError):
        c_obj.create_object_in_db(create_db(), inp)

@moto.mock_dynamodb2
def test_bad_json_forbidden():
    inp = "this is some very bad json"

    with pytest.raises(ValueError):
        c_obj.create_object_in_db(create_db(), inp)
