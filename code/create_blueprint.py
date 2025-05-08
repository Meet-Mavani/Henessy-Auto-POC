import boto3
import json
client=boto3.client('bedrock-data-automation')
schema_json="""
bank_statement_schema = {
    "properties": {
        "account_holder_address": {
            "type": "string",
            "description": "Full address of the account holder including street, city, state and zip code"
        },
        "account_holder_name": {
            "type": "string",
            "description": "Name of the bank account holder"
        },
        "account_number": {
            "type": "string",
            "description": "The account number for which the statement is prepared"
        },
        "account_summary": {
            "type": "array",
            "description": "Summary of account details"
        },
        "account_type": {
            "type": "string",
            "description": "Type of the bank account, such as 'Checking', 'Savings', etc."
        },
        "bank_name": {
            "type": "string",
            "description": "Name of the financial institution"
        },
        "branch_transit_number": {
            "type": "string",
            "description": "The branch transit number"
        },
        "statement_end_date": {
            "type": "string",
            "description": "End date for the statement in MM/DD/YYYY format"
        },
        "statement_start_date": {
            "type": "string",
            "description": "Statement start date in MM/DD/YYYY format"
        },
        "transaction_details": {
            "type": "array",
            "description": "Detailed list of transactions within the statement period"
        }
    },
    "required": [
        "account_holder_address",
        "account_holder_name",
        "account_number",
        "account_type",
        "bank_name",
        "statement_start_date",
        "statement_end_date"
    ]
}

"""
response=client.create_blueprint(
    blueprintName='bank_statement_blueprint',
    type='DOCUMENT',
    blueprintStage='DEVELOPMENT',
    schema=json.dumps(schema_json)
    
)
print(response)