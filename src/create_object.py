import boto3
from typing import TYPE_CHECKING
from uuid import uuid4
import json
import os
if TYPE_CHECKING:
    import botostubs


def create_object_in_db(database, obj):
    database = database # type: botostubs.DynamoDB.Table
    try:
        obj = json.loads(obj)
    except json.decoder.JSONDecodeError:
        raise ValueError("Supplied JSON is invalid")
    if obj.get("uid"):
        raise ValueError("Key 'uid' is not allowed in top level of object.")
    obj["uid"]: str = uuid4().hex
    database.put_item(Item=obj)
    return obj


def handler(event, context):
    dynamo_db = boto3.resource("dynamodb") # type: botostubs.DynamoDB
    table = dynamo_db.Table(os.environ["DYNAMO_DB_TABLE_ARN"])
    try:
        response = create_object_in_db(table, event["body"])
        return {
            "status": 200,
            "body": f"{json.dumps(response)}"
        }
    except ValueError as e:
        return {
            "status": 400,
            "body": f"{e}"
        }
