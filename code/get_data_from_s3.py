import boto3
client=boto3.client('s3')

s3_URL="results//55abe9b3-7885-42cb-9a2c-e428888d73d0/0/custom_output/0/"
client.download_file('bucket-for-henessy', s3_URL,'code/')