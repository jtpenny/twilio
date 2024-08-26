import os
import boto3
import json
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
twiml_table = dynamodb.Table('<table>')

print('hello')
r2 = twiml_table.query(
    KeyConditionExpression=Key('did').eq('*')
)
print(r2)
if len(r2['Items']) == 0:
    with open("twiml.json") as json_file:
        items = json.load(json_file)
        for item in items:
            print(item)
            try:
                twiml_table.put_item(Item=item)
            except Exception as e:
                print(e)

