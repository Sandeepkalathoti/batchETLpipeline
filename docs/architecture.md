# Batch ETL Pipeline Architecture

## Overview

This project implements a batch ETL pipeline for automatically extracting data from MySQL, transforming and cleaning the data, and loading the processed data into Snowflake for analytics.

Apache Airflow is used to orchestrate and schedule the ETL workflow.

## Architecture

```text
                Data Source
                    |
                    v
                  MySQL
                    |
                    v
              Apache Airflow
                    |
                    v
            Data Transformation
                    |
                    v
                Snowflake
                    |
                    v
                Analytics
