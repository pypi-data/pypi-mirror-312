import boto3
from botocore.exceptions import BotoCoreError, ClientError

def publish_to_sns(subject, message, topic_arn, region_name='us-east-1'):
    """
    Publishes a message to an SNS topic.
    """
    sns_client = boto3.client('sns', region_name=region_name)
    try:
        response = sns_client.publish(
            TopicArn=topic_arn,
            Subject=subject,
            Message=message
        )
        return response
    except (BotoCoreError, ClientError) as error:
        raise Exception(f"Failed to publish message to SNS: {str(error)}")
