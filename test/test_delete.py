from mock_db import create_db
from src import delete_object as d_obj
import pytest
import moto
STARTING_DB_INPUT = {
    "uid": "my_uid"
}


@moto.mock_dynamodb2
def test_delete_on_real_object_causes_no_error():
    """
    Deleting an object should cause no error
    """
    db = create_db()
    d_obj.delete_object_from_db(db, "my_uid")
    # assert no errors
    assert not db.get_item(Key={
        "uid": "my_uid"
    }).get("Item", False)


@moto.mock_dynamodb2
def test_multiple_deletes_result_in_no_error():
    """
    Deleting an object multiple times should only ensure that that object doesn't exist (idempotent)
    """
    db = create_db()
    d_obj.delete_object_from_db(db, "my_uid")
    d_obj.delete_object_from_db(db, "my_uid")
    # assert no errors
    assert not db.get_item(Key={
        "uid": "my_uid"
    }).get("Item", False)
