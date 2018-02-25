import boto3
from logs import Logs
import logging
import os


# Create an SNS client
def push_notification(message_header, message_body):
    if not os.path.exists("./logs"):
        os.makedirs("./logs")
    logging.basicConfig(filename='logs/' + Logs.get_log_file_name(),level=logging.INFO)

    client = boto3.client(
        "sns",
        region_name="us-west-2"
    )


    try:
        response = client.publish(
            TopicArn='arn:aws:sns:us-west-2:036218645499:Notification_Bitcoin',
            Subject="[IMPORTANT] Trading Notification",
            Message = message_header + '\n' + message_body
        )
        print 'Pushing notification'
        logging.info('Pushing notification')
        print 'message is:\n %s' % message_header + '\n' + message_body
        print 'response is: %s' % response  
    except:
        print 'Error publishing the message'
        logging.error('Error publishing the message')
        pass
