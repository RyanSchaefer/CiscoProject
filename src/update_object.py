import json
import os
from traceback import print_exc
from typing import TYPE_CHECKING

import boto3
import botocore.exceptions

if TYPE_CHECKING:
    import botostubs


def update_object_in_db(db, uid: str, obj: str) -> dict:
    """
    Updates an object in the DB
    :exception ValueError: if the item does not exist
    :exception ValueError: if the url uid and the objects uid do not match
    :exception ValueError: if the json is invalid
    :param db: the db with put_item
    :param uid: the uid from the url
    :param obj: a json string of what to update the object to
    :return: the updated object
    """
    table = db  # type: botostubs.DynamoDB.DynamodbResource.Table
    obj = json.loads(obj)
    if not obj.get("uid"):
        obj["uid"] = uid
    if obj.get("uid") and obj["uid"] == uid:
        try:
            table.put_item(
                Item=obj,
                ConditionExpression="uid = :uid",
                ExpressionAttributeValues={
                    ':uid': obj["uid"]
                }
            )
            return obj
        except botocore.exceptions.ClientError as e:
            raise ValueError("Item does not exist")
    else:
        raise ValueError("Objects uid and URLS uid do not match")


def handler(event, context):
    """
    Updates an object in the DB
    :param event: the HttpApi Gateway event
    :param context: the lambda context
    :return: a dict that will be parsed into a HTTP response
    """
    dynamo_db = boto3.resource("dynamodb")  # type: botostubs.DynamoDB
    table = dynamo_db.Table(os.environ["DYNAMO_DB_TABLE_ARN"])
    try:
        response = update_object_in_db(table, event["pathParameters"]["object_uid"], event["body"])
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
            },
            "isBase64Encoded": False
        }
