import os
import json
import boto3
import pyodbc
import tempfile
import logging

# Initialize the logger
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def connect_to_sql_server():
    '''
    Establish a connection to SQL Server using pyodbc.
    '''
    try:
        # SQL Server connection details
        server = os.environ['SQL_SERVER_HOST']  # SQL Server Host
        database = os.environ['SQL_DATABASE']   # Database name
        username = os.environ['SQL_USER']       # SQL Server username
        password = os.environ['SQL_PASSWORD']   # SQL Server password
        driver = '{ODBC Driver 17 for SQL Server}'  # ODBC driver for Linux

        # Create connection string
        conn_str = f'DRIVER={driver};SERVER={server};PORT=1433;DATABASE={database};UID={username};PWD={password}'
        
        # Establish connection
        conn = pyodbc.connect(conn_str)
        logger.info("Successfully connected to SQL Server.")
        return conn
    except Exception as e:
        logger.error(f"Error connecting to SQL Server: {str(e)}")
        raise

def download_csv_from_s3(s3_key):
    '''
    Download the CSV file from S3 and return the local path.
    '''
    try:
        s3 = boto3.client("s3")
        s3_bucket_name = os.environ.get('S3_BUCKET_NAME')

        # Create a temporary file
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".csv")
        
        # Download the file from S3
        s3.download_file(s3_bucket_name, s3_key, temp_file.name)
        logger.info(f"File {s3_key} downloaded successfully to {temp_file.name}")
        
        return temp_file.name
    except Exception as e:
        logger.error(f"Error downloading file from S3: {str(e)}")
        raise

def load_csv_into_sql_server(local_file_path):
    '''
    Upload data from CSV file into SQL Server.
    '''
    try:
        conn = connect_to_sql_server()
        cursor = conn.cursor()

        # Open the CSV file and process the data row by row
        with open(local_file_path, 'r') as f:
            # Assuming CSV file has headers, so we skip them
            headers = f.readline().strip().split(',')
            
            for line in f:
                data = line.strip().split(',')
                # Modify the SQL query based on your CSV structure
                query = "INSERT INTO your_table_name (column1, column2, column3) VALUES (?, ?, ?)"
                cursor.execute(query, tuple(data))
        
        conn.commit()
        cursor.close()
        conn.close()
        logger.info(f"Successfully loaded data from {local_file_path} into SQL Server.")
    except Exception as e:
        logger.error(f"Error loading data into SQL Server: {str(e)}")
        raise

def lambda_handler(event, context):
    '''
    AWS Lambda entry point triggered by SQS.
    '''
    try:
        # Get S3 key from the SQS event
        s3_key = event['Records'][0]['s3']['object']['key']
        logger.info(f"Processing file {s3_key}.")

        # Step 1: Download file from S3
        local_file_path = download_csv_from_s3(s3_key)

        # Step 2: Load CSV into SQL Server
        load_csv_into_sql_server(local_file_path)

        return {
            'statusCode': 200,
            'body': f"Successfully loaded {s3_key} into SQL Server."
        }

    except Exception as e:
        logger.error(f"Lambda failed: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error processing {event.get('s3_key')}. Error: {str(e)}"
        }