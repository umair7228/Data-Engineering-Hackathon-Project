import requests
from bs4 import BeautifulSoup
import boto3
from io import StringIO
import datetime
import csv
import json

def lambda_handler(event=None, context=None):
    url = "https://coinmarketcap.com/"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    }

    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')

    tbody = soup.find('tbody')
    if not tbody:
        raise Exception("Table body not found")

    rows = tbody.find_all('tr')
    if not rows:
        raise Exception("No rows found in the crypto table")

    data = []
    timestamp = datetime.datetime.utcnow().isoformat()

    for row in rows[:10]:
        cols = row.find_all('td')
        if len(cols) < 10:
            continue

        name_col = cols[2]
        name_tag = name_col.find('p')
        name = name_tag.text.strip() if name_tag else ""
        symbol_tag = name_col.find_all('p')
        symbol = symbol_tag[1].text.strip() if len(symbol_tag) > 1 else ""

        price = cols[3].text.strip()
        change_1h = cols[4].text.strip()
        change_24h = cols[5].text.strip()
        change_7d = cols[6].text.strip()
        market_cap = cols[7].text.strip()
        volume_24h = cols[8].text.strip()
        circulating_supply = cols[9].text.strip()

        data.append({
            "timestamp": timestamp,
            "source": "coinmarketcap",
            "name": name,
            "symbol": symbol,
            "price": price,
            "1h %": change_1h,
            "24h %": change_24h,
            "7d %": change_7d,
            "market_cap": market_cap,
            "volume_24h": volume_24h,
            "circulating_supply": circulating_supply,
            "status": "success"
        })

    now = datetime.datetime.utcnow()
    bucket = "data-hackathon-smit-umair"
    time_prefix = f"{now.year}/{now.month:02d}/{now.day:02d}/{now.hour:02d}{now.minute:02d}"

    s3 = boto3.client("s3")

    # Step 1: Upload raw JSON
    raw_key = f"raw/coinmarketcap/{time_prefix}.json"
    s3.put_object(
        Bucket=bucket,
        Key=raw_key,
        Body=json.dumps(data),
        ContentType="application/json"
    )

    # Step 2: Transform to CSV
    csv_buffer = StringIO()
    fieldnames = [
        "timestamp", "source", "name", "symbol", "price",
        "1h %", "24h %", "7d %", "market_cap",
        "volume_24h", "circulating_supply", "status"
    ]
    writer = csv.DictWriter(csv_buffer, fieldnames=fieldnames)
    writer.writeheader()
    writer.writerows(data)

    # Step 3: Upload processed CSV
    processed_key = f"processed/coinmarketcap/{time_prefix}.csv"
    s3.put_object(
        Bucket=bucket,
        Key=processed_key,
        Body=csv_buffer.getvalue(),
        ContentType="text/csv"
    )

    return {
        "statusCode": 200,
        "body": f"✅ Raw JSON saved to s3://{bucket}/{raw_key}, CSV saved to s3://{bucket}/{processed_key}"
    }