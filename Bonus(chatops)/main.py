import boto3
import json
import json
import boto3

# Initialize boto3 clients
sns_client = boto3.client('sns')
lambda_client = boto3.client('lambda')
ses_client = boto3.client('ses')

# Create SNS topics
def create_sns_topics():
    topics = ['deployment_success', 'deployment_failure']
    topic_arns = {}
    for topic in topics:
        response = sns_client.create_topic(Name=topic)
        topic_arns[topic] = response['TopicArn']
    return topic_arns

# Create Lambda function
def create_lambda_function():
    lambda_code = """

sns_client = boto3.client('sns')

def lambda_handler(event, context):
    message = event['message']
    topic_arn = event['topic_arn']
    sns_client.publish(
        TopicArn=topic_arn,
        Message=message
    )
    return {
        'statusCode': 200,
        'body': json.dumps('Notification sent!')
    }
"""
    response = lambda_client.create_function(
        FunctionName='ChatOpsNotification',
        Runtime='python3.8',
        Role='arn:aws:iam::YOUR_ACCOUNT_ID:role/YOUR_LAMBDA_ROLE',
        Handler='index.lambda_handler',
        Code={'ZipFile': lambda_code.encode('utf-8')},
        Timeout=15,
        MemorySize=128
    )
    return response['FunctionArn']

# Configure SES
def configure_ses():
    response = ses_client.verify_email_identity(
        EmailAddress='your-email@example.com'
    )
    return response

if __name__ == "__main__":
    topic_arns = create_sns_topics()
    lambda_arn = create_lambda_function()
    ses_response = configure_ses()
    print("SNS Topics:", topic_arns)
    print("Lambda ARN:", lambda_arn)
    print("SES Response:", ses_response)