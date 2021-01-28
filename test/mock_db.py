import moto
import boto3
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    import botostubs

@moto.mock_dynamodb2
def create_db(objects=None):
    if objects is None:
        objects = []
    client = boto3.resource("dynamodb", "us-east-1")  # type: botostubs.DynamoDB.DynamodbResource
    table = client.create_table(
        TableName="mock",
        KeySchema=[
            {
                'AttributeName': 'uid',
                'KeyType': 'HASH'
            },
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'uid',
                'AttributeType': 'S'
            },
        ],
    )  # type: botostubs.DynamoDB.DynamodbResource.Table
    for obj in objects:
        table.put_item(Item=obj)
    return table
