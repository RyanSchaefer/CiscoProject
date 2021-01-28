from mock_db import create_db
from src import delete_object as d_obj
import pytest
import moto
STARTING_DB_INPUT = {
    "uid": "my_uid"
}

@moto.mock_dynamodb2
def test_delete_on_real_object_causes_no_error():
    db = create_db()
    d_obj.delete_object_from_db(db, "my_uid")
    # assert no errors
    assert True

@moto.mock_dynamodb2
def test_error_on_delete_of_non_existent_object():
    db = create_db()
    with pytest.raises(ValueError):
        d_obj.delete_object_from_db(db, "I don't exist!")
