import boto3
from boto3.dynamodb.types import TypeDeserializer
from typing import TYPE_CHECKING
import os

if TYPE_CHECKING:
    import botostubs
    from typing import Iterator


def get_single_object_from_db(db, url, uid):
    table = db  # type: botostubs.DynamoDB.DynamodbResource.Table
    response = table.get_item(Key={
        "uid": uid
    })
    if response.get("Item"):
        return response["Item"]
    else:
        raise ValueError("Key does not exist")


def handle_single(event, context):
    dynamo_db = boto3.client("dynamodb")  # type: botostubs.DynamoDB
    paginator = dynamo_db.get_paginator("scan").paginate(
        TableName=os.environ["DYNAMO_DB_TABLE_ARN"]
    )
    print(event)
    return {
        "status": 200,
        "body": get_all_object_links_from_db(
            paginator,
            f"{event['requestContext']['domainName']}{event['requestContext']['http']['path']}"
        )
    }

def get_all_object_links_from_db(paginator, url):
    database = paginator  # type: botostubs.DynamoDB.ScanOutput
    items = []
    deserializer = TypeDeserializer()
    for page in paginator:
        for item in page["Items"]:
            item = {k: deserializer.deserialize(v) for k, v in item.items()}
            items.append({"url": f"{url}/{item['uid']}"})
    return items


def handle_multiple(event, context):
    dynamo_db = boto3.client("dynamodb")  # type: botostubs.DynamoDB
    paginator = dynamo_db.get_paginator("scan").paginate(
        TableName=os.environ["DYNAMO_DB_TABLE_ARN"]
    )
    print(event)
    return {
        "status": 200,
        "body": get_all_object_links_from_db(
            paginator,
            f"{event['requestContext']['domainName']}{event['requestContext']['http']['path']}"
        )
    }

