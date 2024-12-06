import boto3
from botocore.exceptions import BotoCoreError, ClientError

def send_message_to_sqs(queue_url, message_body, message_attributes=None, region_name='us-east-1'):
    """
    Sends a message to an SQS queue.
    """
    sqs_client = boto3.client('sqs', region_name=region_name)
    try:
        response = sqs_client.send_message(
            QueueUrl=queue_url,
            MessageBody=message_body,
            MessageAttributes=message_attributes or {}
        )
        return response
    except (BotoCoreError, ClientError) as error:
        raise Exception(f"Failed to send message to SQS: {str(error)}")
