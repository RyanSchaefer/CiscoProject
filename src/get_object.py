import json
import os
from typing import TYPE_CHECKING

import boto3
from boto3.dynamodb.types import TypeDeserializer

if TYPE_CHECKING:
    import botostubs


def get_single_object_from_db(db, uid: str) -> dict:
    """
    Gets one object from a DB based on its uid
    :exception ValueError: if the key does not exist
    :param db: the db with get_item to get from
    :param uid: the uid of the object
    :return: the object
    """
    table = db  # type: botostubs.DynamoDB.DynamodbResource.Table
    response = table.get_item(Key={
        "uid": uid
    })
    if response.get("Item"):
        return response["Item"]
    else:
        raise ValueError("Key does not exist")


def handle_single(event: dict, context) -> dict:
    """
    Lambda to handle a single get request
    :param event: the HttpApi Gateway event
    :param context: the lambda context
    :return: a dict that will be parsed into a HTTP response
    """
    dynamo_db = boto3.resource("dynamodb")  # type: botostubs.DynamoDB.DynamodbResource
    table = dynamo_db.Table(os.environ["DYNAMO_DB_TABLE_ARN"])
    try:
        return {
            "statusCode": 200,
            "body": json.dumps(get_single_object_from_db(
                table,
                f"{event['pathParameters']['object_uid']}"
            )),
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


def get_all_object_links_from_db(paginator, url: str) -> dict:
    """
    Gets all objects from a db
    :param paginator: a dynamodb scan paginator
    :param url: the base url for an api get request
    :return: the object
    """
    database = paginator  # type: botostubs.DynamoDB.ScanOutput
    items = []
    deserializer = TypeDeserializer()
    for page in paginator:
        for item in page["Items"]:
            item = {k: deserializer.deserialize(v) for k, v in item.items()}
            items.append({"url": f"{url}/{item['uid']}"})
    return items


def handle_multiple(event: dict, context) -> dict:
    """
    Handles getting all available objects from the DB
    :param event: the HttpApi Gateway event
    :param context: the lambda context
    :return: a dict that will be parsed into a HTTP response
    """
    dynamo_db = boto3.client("dynamodb")  # type: botostubs.DynamoDB
    paginator = dynamo_db.get_paginator("scan").paginate(
        TableName=os.environ["DYNAMO_DB_TABLE_ARN"]
    )
    print(event)
    return {
        "statusCode": 200,
        "body": json.dumps(get_all_object_links_from_db(
            paginator,
            f"{event['requestContext']['domainName']}{event['requestContext']['http']['path']}"
        )),
        "headers": {
            'Content-Type': 'application/json'
        },
        "isBase64Encoded": False
    }
