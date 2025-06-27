import os
import boto3
from snowflake_provider import Provider
from datetime import datetime
import tempfile

def connect_to_snowflake():
    '''
    Building connection with Snowflake using custom Provider class.
    '''
    params = {
        'region_name': os.environ['region_name'],
        'aws_db_creds_secret_id': 'db/currency-echange-rate',
        'aws_db_creds_secret_value': 'fusion_snowflake',
        'snowflake_db': os.environ['snowflake_db'],
        'snowflake_role': os.environ['snowflake_role'],
        'snowflake_wh': os.environ['snowflake_wh'],
        'environment': os.environ['environment']
    }

    provider = Provider(**params)
    return provider

def download_csv_from_s3(s3_key):
    '''
    Download the CSV file from S3 and return the local path.
    '''
    s3 = boto3.client("s3")
    s3_bucket_name = os.environ.get('s3_bucket_name')

    temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
    s3.download_file(s3_bucket_name, s3_key, temp_file.name)
    return temp_file.name

def load_csv_into_snowflake(local_file_path, table_name="stock_data", schema_name="PUBLIC"):
    '''
    Upload file to Snowflake stage and execute COPY INTO to load into target table.
    '''
    provider = connect_to_snowflake()

    stage_name = f"{schema_name}.internal_stage"
    provider.exe_query(f"CREATE STAGE IF NOT EXISTS {stage_name};")

    # Upload file to stage
    provider.upload_file_to_stage(stage_name, local_file_path)

    copy_sql = f"""
    COPY INTO {schema_name}.{table_name}
    FROM @{stage_name}/{os.path.basename(local_file_path)}
    FILE_FORMAT = (TYPE = 'CSV' FIELD_OPTIONALLY_ENCLOSED_BY = '"' SKIP_HEADER = 1)
    ON_ERROR = 'CONTINUE';
    """

    provider.exe_query(copy_sql)

def lambda_handler(event, context):
    '''
    AWS Lambda entry point.
    '''
    # Get S3 key from event or define manually for testing
    s3_key = event.get('s3_key') or 'yahoofinance/2025/05/23/0930.csv'

    # Step 1: Download file from S3
    local_file_path = download_csv_from_s3(s3_key)

    # Step 2: Load CSV into Snowflake
    load_csv_into_snowflake(local_file_path)

    return {
        'statusCode': 200,
        'body': f"Successfully loaded {s3_key} into Snowflake."
    }