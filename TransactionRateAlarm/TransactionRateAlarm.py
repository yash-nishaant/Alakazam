from __future__ import print_function
import boto3
import base64

client = boto3.client('sns')
# Include your SNS topic ARN here.
# your topic here
topic_arn = 'arn:aws:sns:eu-central-1:************<your-account-id>:AlakazamAlarms'


def lambda_handler(event, context):
    try:
        client.publish(TopicArn=topic_arn, Message='Investigate sudden surge in orders',
                       Subject='Alakazam Order Rate Alarm')
        print('Successfully delivered alarm message')
    except Exception:
        print('Delivery failure')
