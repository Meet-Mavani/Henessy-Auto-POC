import boto3

client=boto3.client('bedrock-data-automation')

response=client.create_data_automation_project(
    projectName="testing_project",
    projectDescription="This project is for the validation of the document",
    projectStage="DEVELOPMENT",
    standardOutputConfiguration={
        'document':{
            'extraction':{
                'granularity':{
                    'types':[
                        'PAGE',
                    ]
                },
                'boundingBox':{
                    'state':'ENABLED'
                }
            },
            'generativeField':{
                'state':'ENABLED'
            },
            'outputFormat':{
                'textFormat':{
                    'types':[
                        'MARKDOWN',
                    ]
                },
                'additionalFileFormat':{
                    'state':'ENABLED'
                }
            }
        },
        'image': {
            'extraction': {
                'category': {
                    'state': 'ENABLED',
                    'types': [
                       'TEXT_DETECTION',
                    ]
                },
                'boundingBox': {
                    'state': 'ENABLED'
                }
            },
            'generativeField': {
                'state': 'ENABLED',
                'types': [
                    'IMAGE_SUMMARY',
                ]
            }
        },  
    },
    customOutputConfiguration={
        'blueprints': [
            {
                'blueprintArn': 'arn:aws:bedrock:us-east-1:050752609444:blueprint/9c6933e98655',
                'blueprintVersion': '1',
                'blueprintStage': 'LIVE'
            },
        ]
    },
    
    
)