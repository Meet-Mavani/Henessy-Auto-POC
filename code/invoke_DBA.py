## do not run directly

import boto3
import json
import re
client=boto3.client('bedrock-data-automation-runtime')

response=client.invoke_data_automation_async(
    inputConfiguration={
        's3Uri': 's3://bucket-for-henessy/bank_stmt_0.png'
    },
    outputConfiguration={
        's3Uri': 's3://bucket-for-henessy/results/'
    },
    dataAutomationConfiguration={
        'dataAutomationProjectArn': 'arn:aws:bedrock:us-east-1:050752609444:data-automation-project/736764fec041',
        'stage': 'LIVE'
    },
     blueprints=[
        {
            'blueprintArn': 'arn:aws:bedrock:us-east-1:050752609444:blueprint/9c6933e98655',
            'version': '1',
            'stage':'LIVE'
        },
    ],
     dataAutomationProfileArn='arn:aws:bedrock:us-east-1:050752609444:data-automation-profile/us.data-automation-v1',
    
)
print(response)
temp='arn:aws:bedrock:us-east-1:050752609444:data-automation-invocation/55abe9b3-7885-42cb-9a2c-e428888d73d0'

response1 = client.get_data_automation_status(
    invocationArn=temp
)
s3url=response1['outputConfiguration']['s3Uri']

match = re.search(r'([a-f0-9\-]{36})', s3url)
uuid=''
if match:
    uuid1 = match.group(1)
    print(uuid1)
#s3://bucket-for-henessy/results//55abe9b3-7885-42cb-9a2c-e428888d73d0/0/custom_output/0/result.json
#s3://bucket-for-henessy/results//55abe9b3-7885-42cb-9a2c-e428888d73d0/0/custom_output/0/result.json
final_required_s3=f"s3://bucket-for-henessy/results//{uuid1}/0/custom_output/0/result.json"
print(final_required_s3)

