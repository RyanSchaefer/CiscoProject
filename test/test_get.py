import pytest
from src import get_object as g_obj
from mock_db import create_db
import moto
import boto3

STARTING_DB_INPUT = [
    {
        "uid": "some_uid",
        "firstName": "Andrey",
        "lastName": "Kolmogorov",
        "dob": "25 April 1903"
    }
]

BASE_URL = "https://myapp.com/api/objects"


@moto.mock_dynamodb2
def test_get_one_valid_obj():
    """
    Getting a valid object
    """
    db = create_db(STARTING_DB_INPUT)
    actual: dict = g_obj.get_single_object_from_db(db, "some_uid")
    assert actual == STARTING_DB_INPUT[0]


@moto.mock_dynamodb2
def test_get_all_valid_objs():
    """
    Getting all objects
    """
    db = create_db(STARTING_DB_INPUT)
    db.put_item(Item={
        "uid": "another_uid",
        "data": "something"
    })
    paginator = boto3.client("dynamodb", 'us-east-1').get_paginator("scan").paginate(TableName=db.table_name)
    actual = map(lambda x: x["url"], g_obj.get_all_object_links_from_db(paginator, BASE_URL))
    assert set(actual) == {
        f"{BASE_URL}/another_uid",
        f"{BASE_URL}/some_uid"
    }

@moto.mock_dynamodb2
def test_get_invalid_obj():
    """
    Getting an object that doesn't exist
    """
    db = create_db()
    with pytest.raises(ValueError):
        g_obj.get_single_object_from_db(
            db,
            "bad uid"
        )
