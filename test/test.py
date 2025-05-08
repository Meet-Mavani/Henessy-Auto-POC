from textractcaller.t_call import call_textract
from textractprettyprinter.t_pretty_print import Textract_Pretty_Print, get_string
import boto3
import uuid
import time
import json

# AWS clients
client = boto3.client('bedrock-runtime')
client_agent = boto3.client('bedrock-agent')
client_agent_runtime = boto3.client('bedrock-agent-runtime')

# Configuration
data_bucket = 'bucket-for-henessy'  # Bucket name
names = ['ZBSA', 'SBI', 'Account-Opening']  # Names to match in document names

def wait_until_agent_prepared(agent_id, timeout=300, interval=10):
    """Wait for an agent to reach the PREPARED state"""
    print(f"⏳ Waiting for agent {agent_id} to be prepared...")
    start = time.time()
    while time.time() - start < timeout:
        response = client_agent.get_agent(agentId=agent_id)
        status = response['agent']['agentStatus']
        print(f"   → Current status: {status}")
        if status == "PREPARED":
            print("✅ Agent is prepared.")
            return True
        elif status == "FAILED":
            raise Exception("❌ Agent failed to prepare.")
        time.sleep(interval)
    raise TimeoutError("⏰ Timeout: Agent was not prepared within expected time.")

def prepare_agent(agent_id):
    """Prepare an agent for usage"""
    print(f"Preparing agent {agent_id}...")
    response = client_agent.prepare_agent(
        agentId=agent_id
    )
    return response

def textract_extract_text(document, bucket=data_bucket):
    """Extract text from a document using Amazon Textract"""
    try:
        print(f'Processing document: {document}')
        
        # Using amazon-textract-caller
        response = call_textract(input_document=f's3://{bucket}/{document}')
        
        # Using pretty printer to get all the lines
        lines = get_string(textract_json=response, output_type=[Textract_Pretty_Print.LINES])
        
        # Find which name from our list is in the document name
        label = [name for name in names if name in document]
        if not label:
            print(f"Warning: No matching name found in document {document}")
            label = ["Unknown"]
        
        return {
            "label": label[0],
            "text": lines
        }
    except Exception as e:
        print(f"Error processing document: {e}")
        return {
            "label": "Error",
            "text": f"Failed to process: {str(e)}"
        }

def create_agent():
    """Create a new Bedrock agent"""
    response = client_agent.create_agent(
        agentCollaboration='DISABLED',
        agentName='formatter-agent',
        clientToken=str(uuid.uuid4()) + str(uuid.uuid4())[:1],
        agentResourceRoleArn='arn:aws:iam::050752609444:role/service-role/AmazonBedrockExecutionRoleForAgents_K9NKO87SH3',
        description='This agent is used to format data given by Textract',
        foundationModel='amazon.nova-lite-v1:0',
        instruction='You will get the raw data as an input and your task is to map the associated data with their related labels',
        orchestrationType='DEFAULT',
    )
    return response

def create_agent_alias(name, agent_id):
    """Create an alias for an agent"""
    try:
        response = client_agent.create_agent_alias(
            agentAliasName=name,
            agentId=agent_id
        )
        agent_alias = response['agentAlias']
        return agent_alias
    except Exception as e:
        raise Exception(f'Cannot create agent alias: {str(e)}')

def invoke_agent(data, alias_id, agent_id):
    """Invoke an agent with the provided data"""
    try:
        # Convert data to a JSON string if it's a dictionary
        if isinstance(data, dict):
            input_text = json.dumps(data)
        else:
            input_text = str(data)
        
        # Use the dedicated agent runtime client for invoking agents
        response = client_agent_runtime.invoke_agent(
            agentAliasId=alias_id,
            agentId=agent_id,
            inputText=input_text,
            sessionId=str(uuid.uuid4())
        )
        return response
    except Exception as e:
        print(f"Error invoking agent: {e}")
        return None

if __name__ == "__main__":
    # Document to process
    document_name = 'ZBSA-filled-SBI-Account-Opening-Form-for-Non-Individuals-zbsa-1-2.pdf'
    
    # Step 1: Extract text from document
    extracted_data = textract_extract_text(document_name)
    print(f"Extracted data with label: {extracted_data['label']}")
    
    # Step 2: Create or use an existing agent
    # Uncomment if you need to create a new agent
    # agent_response = create_agent()
    # agent_id = agent_response['agent']['agentId']
    # print(f"Created new agent with ID: {agent_id}")
    
    # Using existing agent ID
    agent_id = 'ROO8LTM9KT'
    
    # Step 3: Prepare the agent (uncomment if needed)
    # prepare_response = prepare_agent(agent_id)
    # wait_until_agent_prepared(agent_id)
    
    # Step 4: Create alias or use existing alias
    # Uncomment if you need to create a new alias
    # alias_response = create_agent_alias("first1", agent_id)
    # alias_id = alias_response['agentAliasId']
    # print(f"Created new alias with ID: {alias_id}")
    
    # Using existing alias ID
    alias_id = 'CMF55AI2KX'
    
    # Step 5: Invoke the agent with the extracted data
    result = invoke_agent(extracted_data, alias_id, agent_id)
    
    # Print the result
    if result:
        print("Agent Response:")
        if 'completion' in result:
            print(result['completion'])
        else:
            print(json.dumps(result, indent=2))
    else:
        print("No response from agent.")
        
        
        
