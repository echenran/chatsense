import boto3
import json
import decimal
from boto3.dynamodb.conditions import Key, Attr

dynamodb = boto3.resource('dynamodb', region_name='us-east-2', aws_access_key_id='AKIAIO5FODNN7EXAMPLE', aws_secret_access_key='ABCDEF+c2L7yXeGvUyrPgYsDnWRRC1AYEXAMPLE')

table=dynamodb.Table('messages')

table.query(KeyConditionExpression=Key('userKey').eq('Amy+Jake'))

