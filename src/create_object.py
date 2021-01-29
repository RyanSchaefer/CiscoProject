import json
import os
from typing import TYPE_CHECKING
from uuid import uuid4

import boto3

if TYPE_CHECKING:
    import botostubs


def create_object_in_db(database, obj: str) -> dict:
    """
    Creates an object on the supplied db
    :exception ValueError: if the object is invalid json or the key "uid" exists (users should not be allowed to specify
    a uid)
    :param database: a database object that can put_item
    :param obj: a json-like string
    :return: the object placed in the db with a new "uid" key
    """
    database = database  # type: botostubs.DynamoDB.Table
    try:
        obj = json.loads(obj)
    except json.decoder.JSONDecodeError:
        raise ValueError("Supplied JSON is invalid")
    if obj.get("uid"):
        raise ValueError("Key 'uid' is not allowed in top level of object.")
    obj["uid"]: str = uuid4().hex
    database.put_item(Item=obj)
    return obj


def handler(event: dict, context) -> dict:
    """
    The lambda handler
    :param event: the HttpApi Gateway event
    :param context: the lambda context
    :return: a dict that will be parsed into a HTTP response
    """
    dynamo_db = boto3.resource("dynamodb")  # type: botostubs.DynamoDB
    table = dynamo_db.Table(os.environ["DYNAMO_DB_TABLE_ARN"])
    try:
        response = create_object_in_db(table, event["body"])
        return {
            "statusCode": 200,
            "body": json.dumps(response),
            "headers": {
                'Content-Type': 'application/json'
            },
            "isBase64Encoded": False
        }
    except ValueError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({
                "error": str(e)
            }),
            "headers": {
                'Content-Type': 'application/json'
            }
        }
