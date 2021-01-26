from mock_db import MockDatabase
from src import delete_object as d_obj
import pytest

STARTING_DB_INPUT = {
    "uid": "my_uid"
}


def test_delete_on_real_object_causes_no_error():
    db = MockDatabase(STARTING_DB_INPUT)
    d_obj.handle_helper(db, "my_uid")
    # assert no errors
    assert True


def test_error_on_delete_of_non_existent_object():
    db = MockDatabase()
    with pytest.raises(ValueError):
        d_obj.handle_helper(db, "I don't exist!")
