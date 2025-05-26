from fastapi import FastAPI
from function111.bedrockClient import create_s3_client_from_bedrock,fetch_result_from_s3,invoke_bedrock_data_automation
from typing import Optional
app=FastAPI()

@app.get("/")
async def get_started():
    return {"message":"Hello Guys"}


def compare_result(cached_result):
    
    if cached_result is None:
        return {"erroe":"Please first load the data"}
    expected_keys={"transaction_details","statement_start_date","statement_end_date","branch_transit_number","bank_name","account_type","account_summary","account_number","account_holder_name","account_holder_address"}
    actual_keys=set(cached_result.keys())
    
    match= actual_keys == expected_keys
   
    data={
        "match": match,
        "actual_keys": list(actual_keys),
        "expected_keys": list(expected_keys),
        "missing_keys": list(expected_keys - actual_keys),
        "extra_keys": list(actual_keys - expected_keys),
    }
    print(data)


@app.get("/get-result/")
def get_result():
    global cached_result
    try:
        s3_url = invoke_bedrock_data_automation(
            's3://bucket-for-henessy/bank_stmt_0.png',
            's3://bucket-for-henessy/results/'
        )
        print("stopped here")
        print(f"Returned S3 URL: {s3_url}")
        
        print("Calling fetch_result_from_s3...")
        cached_result = fetch_result_from_s3(s3_url)
        print(f"Fetched Result: {cached_result}")
        
        try:
            compare_result(cached_result)
        except Exception as e:
            print(f"Error in compare_result: {e}")
        
        return {"data": cached_result}
    
    except Exception as e:
        print(f"Unexpected Error: {e}")
        return {"error": str(e)}
