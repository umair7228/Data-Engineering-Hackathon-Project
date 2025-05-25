# 🚀 DataPulse: Real-Time Serverless Data Ingestion Pipeline

**DataPulse** is a real-time, serverless data pipeline built using AWS services. It automates the ingestion and processing of financial, cryptocurrency, and foreign exchange data from three different sources. The system fetches and stores raw data every minute using AWS Lambda, EventBridge, and S3, with optional transformation steps for certain datasets.

---

## 📚 Table of Contents

- [Overview](#overview)
- [Architecture](#architecture)
- [Data Sources](#data-sources)
- [AWS Services Used](#aws-services-used)
- [S3 Storage Format](#s3-storage-format)
- [Project Structure](#project-structure)
- [Setup & Deployment](#setup--deployment)

---

## 🧠 Overview

This project demonstrates how to:

- Ingest real-time data from Yahoo Finance, CoinMarketCap, and Open Exchange Rates.
- Use **AWS Lambda** functions triggered every minute via **Amazon EventBridge**.
- Save raw data to an **S3 bucket** under organized folders by source and timestamp.
- Transform CoinMarketCap data and store it in a `proceed/` folder.

---

## 📦 Architecture

```
 ┌────────────────────────────────────────┐
 │           Amazon EventBridge           │
 │        (Triggers every minute)         │
 └──────────────┬───────────────┬─────────┘
                ↓               ↓
       ┌──────────────┐ ┌────────────────┐
       │ Lambda:      │ │ Lambda:        │
       │ YahooFinance │ │ CoinMarketCap  │
       └──────┬───────┘ └──────┬──────────┘
              ↓               ↓
       s3://bucket/raw/  s3://bucket/raw/
              ↓               ↓
           (Optional)   Lambda: Transform
                             ↓
                s3://bucket/transformed/
                                 ↓
                       CoinMarketCap data
```

---

## 🌍 Data Sources

### 1. Yahoo Finance
- **Library:** `yfinance`
- **Data:** OHLCV (Open, High, Low, Close, Volume) for all S&P 500 symbols
- **Trigger:** Every 1 minute
- **Storage Path:**
  ```
  s3://data-hackathon-smit-{yourname}/raw/yahoofinance/YYYY/MM/DD/HHMM.json
  ```

### 2. CoinMarketCap
- **Libraries:** `requests`, `BeautifulSoup`
- **Data:** Top 10 cryptocurrencies by market cap
- **Trigger:** Every 1 minute
- **Storage Paths:**
  ```
  Raw:        s3://data-hackathon-smit-{yourname}/raw/coinmarketcap/YYYY/MM/DD/HHMM.json
  Transformed: s3://data-hackathon-smit-{yourname}/transformed/coinmarketcap/YYYY/MM/DD/HHMM.json
  ```

### 3. Open Exchange Rates
- **API:** https://openexchangerates.org/
- **Data:** Real-time foreign exchange rates
- **Trigger:** Every 1 minute
- **Storage Path:**
  ```
  s3://data-hackathon-smit-{yourname}/raw/openexchangerates/YYYY/MM/DD/HHMM.json
  ```

---

## ☁️ AWS Services Used

- **AWS Lambda** – For fetching and transforming data
- **Amazon EventBridge** – To trigger Lambda functions every minute
- **Amazon S3** – To store raw and transformed data
- *(SNS and SQS FIFO Queues mentioned in the design, but not implemented)*

---

## 🗂️ S3 Storage Format

Each S3 object is saved in the following structure:
```
s3://data-hackathon-smit-{yourname}/
  └── raw/
      ├── yahoofinance/
      ├── coinmarketcap/
      └── openexchangerates/
  └── transformed/
      └── coinmarketcap/
```

Each file includes:
- Timestamp
- Source Name
- Symbol (if applicable)
- Response Status (HTTP)

---

## 🏗️ Project Structure

```
📁 src/
 ├── lambda_yahoofinance/
 │   └── handler.py
 ├── lambda_coinmarketcap/
 │   └── handler.py
 ├── lambda_openexchangerates/
 │   └── handler.py
 └── transform_coinmarketcap/
     └── handler.py

📁 data/
 ├── raw/
 │   ├── yahoofinance/
 │   ├── coinmarketcap/
 │   └── openexchangerates/
 └── transformed/
     └── coinmarketcap/

📄 README.md
```

---

## ⚙️ Setup & Deployment

### 1. Create S3 Bucket
```bash
aws s3 mb s3://data-hackathon-smit-yourname
```

### 2. Deploy Lambda Functions
Each function should be uploaded via the AWS Console or using the AWS CLI with appropriate IAM roles for S3 access.

### 3. Configure EventBridge Triggers
Set up EventBridge rules to invoke each Lambda function every minute.

---

## 📜 License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for more details.

---

## 🙌 Acknowledgments

Built during the **Saylani Mass IT Training - Data Engineering Hackathon** under the guidance of **Sir Qasim Hassan**.

---