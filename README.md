# 🚀 DataPulse: Real-Time Serverless Data Ingestion Pipeline

**DataPulse** is a real-time, serverless data pipeline built using AWS services. It automates the ingestion and processing of financial, cryptocurrency, and foreign exchange data from three different sources. The system fetches and stores raw data every minute using AWS Lambda, EventBridge, and S3, with optional transformation steps for certain datasets.

---

## 📚 Table of Contents

- [Overview](#overview)
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

## 🌍 Data Sources

### 1. Yahoo Finance
- **Library:** `yfinance`
- **Data:** OHLCV (Open, High, Low, Close, Volume) for all S&P 500 symbols
- **Trigger:** Every 1 minute

### 2. CoinMarketCap
- **Libraries:** `requests`, `BeautifulSoup`
- **Data:** Top 10 cryptocurrencies by market cap
- **Trigger:** Every 1 minute

### 3. Open Exchange Rates
- **API:** https://openexchangerates.org/
- **Data:** Real-time foreign exchange rates
- **Trigger:** Every 1 minute

---

## ☁️ AWS Services Used

- **AWS Lambda** – For fetching and transforming data
- **Amazon EventBridge** – To trigger Lambda functions every minute
- **Amazon S3** – To store raw and transformed data

---

## 🙌 Acknowledgments

Built during the **Saylani Mass IT Training - Data Engineering Hackathon** under the guidance of **Sir Qasim Hassan**.

---
