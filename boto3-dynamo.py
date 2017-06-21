from __future__ import print_function  # Python 2/3 compatibility
import boto3
import datetime

dynamodb = boto3.resource('dynamodb', region_name='us-west-2')


def db_initproject(tablename):
    try:
        table = dynamodb.create_table(
            TableName=tablename,
            KeySchema=[
                {
                    'AttributeName': 'job-id',
                    'KeyType': 'HASH'
                }
            ],
            AttributeDefinitions=[
                {
                    'AttributeName': 'job-id',
                    'AttributeType': 'S'
                }

            ],
            ProvisionedThroughput={
                'ReadCapacityUnits': 5,
                'WriteCapacityUnits': 5,
            }
        )
        print('Creating new [{}]'.format(tablename))
        table.meta.client.get_waiter('table_exists').wait(TableName=tablename)
    except Exception as notable:
        if notable:
            print('Adding to existing [{}]'.format(tablename))
            table = dynamodb.Table(tablename)
            table.meta.client.get_waiter('table_exists').wait(TableName=tablename)

    return table


def db_item(table, name, owner, test_config, job_status):
    job_id = '{}-{}'.format(name, datetime.datetime.now().strftime("%Y%m%d%s"))
    log_stream = "{}-{}".format(name, job_id)
    table.put_item(
        Item={
            'job-id': job_id,
            'owner': owner,
            'log-group': name,
            'job-config': test_config,
            'job-status': job_status,
            'log-stream': log_stream,
        }
    )


new_project = db_initproject('project-name')
db_item(new_project, 'prj-name', 'owner', 'testcfg', 'PASS')
