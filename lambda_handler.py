import boto3
from botocore.exceptions import ClientError
import json
import datetime

def lambda_handler(event, context):
    tmp = event['Records'][0]['Sns']['Message']
    message = eval(tmp)
    
    if message['type'] == "heartbeatAlert" and message['event'] == "HeartbeatOK":
        print("Got HeartBeat Alert so ignored: ", tmp)
    else:
        payload = {"region": "us-east-1", "environment": message['environment'], "severity": message['severity'], "resource": message['resource'].upper(), "text": message['text'], "href": message['href'], "duplicateCount": message['duplicateCount'], "receiveTime": message['receiveTime'], "status": message['status'], "event": message['event'], "origin": message['origin']}
        send_email(payload)

    return True

def send_email(payload):
    CHARSET = "UTF-8"
    SENDER = "Sender Name <devops.marthanda@gmail.com>"
    RECIPIENT = ["python.marthanda@gmail.com"]
    SUBJECT = "ALERT: {}, {}".format(payload['resource'], payload['text'])

    BODY_TEXT = ("Amazon SES Test (Python)\r\n"
                 "This email was sent with Amazon SES using the "
                 "AWS SDK for Python (Boto)."
                )

    BODY_HTML = "<html> <head> <style type='text/css'> td, th{height: 2rem; border: 1px solid #ccc; text-align: center; padding: 0 1rem 0 1rem;}th{background: lightblue; border-color: white;}body{padding: 1rem;}h1{color: #547a9f;}</style> </head>" + """ <body> <h1>{resource},{text}</h1><table> <tr> <th>Status</th> <th>Environment</th> <th>Severity</th> <th>Resource</th> <th>Event</th> <th>Origin</th> <th>DuplicateCount</th> </tr><tr> <td>{status}</td><td>{environment}</td><td>{severity}</td><td>{resource}</td><td>{event}</td><td>{origin}</td><td>{duplicateCount}</td></tr></table> </td></tr></table> </body> </html>""".format(**payload)

    client = boto3.client('ses',region_name=payload["region"])

    try:
        response = client.send_email(
            Destination={
                'ToAddresses': RECIPIENT,
            },
            Message={
                'Body': {
                    'Html': {
                        'Charset': CHARSET,
                        'Data': BODY_HTML,
                    },
                    'Text': {
                        'Charset': CHARSET,
                        'Data': BODY_TEXT,
                    },
                },
                'Subject': {
                    'Charset': CHARSET,
                    'Data': SUBJECT,
                },
            },
            Source=SENDER
        )
    except ClientError as e:
        print(e.response['Error']['Message'])
    else:
        print("Email sent! Message ID:"),
        print(response['MessageId'])

