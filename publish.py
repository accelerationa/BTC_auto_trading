import boto3

# Create an SNS client
def push_notification(message_header, message_body):
    client = boto3.client(
        "sns",
        aws_access_key_id="AKIAJJSMDL6KX23QYRUQ",
        aws_secret_access_key="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",
        region_name="us-west-2"
    )


    try:
        response = client.publish(
            TopicArn='arn:aws:sns:us-west-2:036218645499:Notification_Bitcoin',
            Subject="[IMPORTANT] Trading Notification",
            Message = message_header + '\n' + message_body
        )
        #test
        print 'Pushing notification'
        print 'message is:\n %s' % message_header + '\n' + message_body
        print 'response is: %s' % response  
    except:
        print 'Error publishing the message'
        print response
        pass
