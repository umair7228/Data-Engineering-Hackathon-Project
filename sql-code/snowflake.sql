CREATE DATABASE IF NOT EXISTS YAHOO_DB;
CREATE SCHEMA YAHOO_DB.YAHOO_SCHEMA;

CREATE TABLE stock_data (
    Datetime TIMESTAMP_TZ,
    Open FLOAT,
    High FLOAT,
    Low FLOAT,
    Close FLOAT,
    Volume INTEGER,
    Dividends FLOAT,
    Stock_Splits FLOAT,
    symbol STRING,
    source STRING,
    ingest_timestamp TIMESTAMP_TZ,
    status STRING
);