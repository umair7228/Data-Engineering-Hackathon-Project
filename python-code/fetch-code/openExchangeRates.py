import requests
import boto3
from io import StringIO
import datetime
import csv

def lambda_handler(event=None, context=None):
    # Fetch from Open Exchange Rates JSON API
    API_KEY = "Your_OpenExchangeRates_API_Key" 
    url = f"https://openexchangerates.org/api/latest.json?app_id={API_KEY}"

    response = requests.get(url)
    if response.status_code != 200:
        raise Exception(f"Failed to fetch data. Status code: {response.status_code}, body: {response.text}")

    json_data = response.json()
    rates = json_data.get("rates", {})
    timestamp = datetime.datetime.utcnow().isoformat()

    # Prepare CSV rows
    data = []
    for currency, value in rates.items():
        data.append({
            "timestamp": timestamp,
            "source": "openexchangerates",
            "currency": currency,
            "rate_to_usd": value,
            "status": "success"
        })

    # Write CSV to memory
    csv_buffer = StringIO()
    fieldnames = ["timestamp", "source", "currency", "rate_to_usd", "status"]
    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

    # Save to S3
    now = datetime.datetime.utcnow()
    bucket = "data-hackathon-smit-umair"  # your bucket name
    s3_key = f"raw/openexchangerates/{now.year}/{now.month:02d}/{now.day:02d}/{now.hour:02d}{now.minute:02d}.csv"

    s3 = boto3.client("s3")
    s3.put_object(
        Bucket=bucket,
        Key=s3_key,
        Body=csv_buffer.getvalue(),
        ContentType="text/csv"
    )

    return {
        "statusCode": 200,
        "body": f"Exchange rates saved to s3://{bucket}/{s3_key}"
    }