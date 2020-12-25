import logging
import boto3
import os
import json
import uuid

LOG = logging.getLogger()
LOG.setLevel(logging.INFO)


def main(event, context):
    LOG.info("EVENT: " + json.dumps(event))

    query_string_params = event['queryStringParameters']
    if query_string_params is not None:
        target_url = query_string_params['targetUrl']
        if target_url is not None:
            return create_short_url(event)

    path_parameters = event['pathParameters']
    if path_parameters is not None:
        if path_parameters['proxy'] is not None:
            return read_short_url(event)

    return {
        'statusCode': 200,
        'body': 'usage: ?targetUrl=URL'
    }


def create_short_url(event):
    LOG.info("Create short url")
    # pull out the dynamoDB table name from environment
    table_name = os.environ.get('TABLE_NAME')

    # parse targetURL
    target_url = event['queryStringParameters']['targetUrl']

    # create a unique id (take first 8 characters)
    id = str(uuid.uuid4())[0:8]

    # create item in DynamoDB
    dynamodb = boto3.resource('dynamodb')
    table = dynamodb.Table(table_name)
    table.put_item(Item={
        'id': id,
        'target_url': target_url
    })

    url = "https://" + \
        event["requestContext"]["domainName"] + \
        event["requestContext"]["path"] + id
    
    LOG.info("url: " + url)

    return {
        'statusCode': 200,
        'body': "Created URL: %s" % url
    }


def read_short_url(event):
    LOG.info("read short url")

    id = event['pathParameters']['proxy']
    
    LOG.info("getting url for id: " + id)

    table_name = os.environ.get('TABLE_NAME')

    ddb = boto3.resource('dynamodb')
    table = ddb.Table(table_name)
    response = table.get_item(Key={'id': id})
    LOG.debug("RESPONSE: " + json.dumps(response))

    item = response.get('Item', None)

    if item is None:
        LOG.info("url is not found in database")
        return {
            'statusCode': 400,
            'body': 'No redirect found for ' + id
        }

    LOG.info("url is found in database: " + item.get('target_url'))
    return {
        'statusCode': 301,
        'headers': {'Location': item.get('target_url')},
    }