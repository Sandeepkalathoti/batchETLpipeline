# Batch ETL Pipeline

An automated batch ETL pipeline that extracts data from MySQL, transforms and validates the data using Python, and prepares it for loading into Snowflake. Apache Airflow is used to orchestrate the workflow.

## Project Overview

This project demonstrates a daily batch data engineering workflow.

The pipeline performs:

1. Data extraction from MySQL
2. Data transformation and cleaning
3. Data quality validation
4. Preparation of curated datasets
5. Loading into Snowflake
6. Workflow orchestration using Apache Airflow
7. Automated testing using Pytest
8. CI automation using GitHub Actions

## Architecture

```text
CSV / API
    |
    v
  MySQL
    |
    v
Apache Airflow
    |
    v
Transform
    |
    v
Quality Check
    |
    v
 Snowflake
    |
    v
Analytics
