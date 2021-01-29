import os
from typing import TYPE_CHECKING

import boto3

if TYPE_CHECKING:
    import botostubs


def delete_object_from_db(db, uid: str):
    """
    Delete an object from the db using the specified UID
    :param db: a db with delete_item
    :param uid: the UID to delete
    """
    database = db  # type: botostubs.DynamoDB.DynamodbResource.Table
    database.delete_item(Key={
        "uid": uid
    })


def handler(event: dict, context) -> dict:
    """
    The lambda handler
    :param event: the HttpApi Gateway event
    :param context: the lambda context
    :return: a dict which will be parsed into a HTTP response
    """
    dynamo_db = boto3.resource("dynamodb")  # type: botostubs.DynamoDB
    table = dynamo_db.Table(os.environ["DYNAMO_DB_TABLE_ARN"])
    response = delete_object_from_db(table, event["pathParameters"]["object_uid"])
    return {
        "statusCode": 200,
        "body": f"",
        "headers": {
            'Content-Type': 'application/json'
        },
        "isBase64Encoded": False
    }
