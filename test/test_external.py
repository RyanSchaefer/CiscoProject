import pytest
import requests
import json
import os

URL = "https://b3xkoqdorb.execute-api.us-east-1.amazonaws.com/api/objects"

TEST_OBJECT = {
    "firstName": "Andrey",
    "lastName": "Kolmogorov",
    "dob": "25 April 1903"
}

@pytest.mark.skipif(not os.environ.get("TEST_DEPLOYMENT"), reason="Cannot confirm that API is deployed yet")
def test_crud_operation():
    """
    Creates an object then runs an get, an update, and a delete
    """
    objects_in_storage = len(requests.get(URL).json())
    post_response = requests.post(URL, json=TEST_OBJECT).json()
    uid = post_response["uid"]
    del post_response["uid"]
    assert post_response == TEST_OBJECT

    get_single_response = requests.get(f"{URL}/{uid}").json()
    del get_single_response["uid"]
    assert get_single_response == post_response

    objects_in_storage2 = len(requests.get(URL).json())
    assert objects_in_storage2 == objects_in_storage + 1

    update_response = requests.put(f"{URL}/{uid}", json={
        "new_attr": "thing"
    }).json()
    assert update_response == {
        "new_attr": "thing",
        "uid": uid
    }
    get_single_response_after_update = requests.get(f"{URL}/{uid}").json()
    assert update_response == get_single_response_after_update

    objects_in_storage3 = len(requests.get(URL).json())
    assert objects_in_storage2 == objects_in_storage3

    delete_response = requests.delete(f"{URL}/{uid}")
    assert delete_response.status_code == 200

    get_single_response_after_delete = requests.get(f"{URL}/{uid}")
    assert get_single_response_after_delete.status_code == 400

    objects_in_storage4 = len(requests.get(URL).json())
    assert objects_in_storage4 == objects_in_storage
