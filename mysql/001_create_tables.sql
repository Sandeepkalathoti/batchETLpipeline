-- Batch ETL Pipeline
-- MySQL source database schema

CREATE DATABASE IF NOT EXISTS batch_etl_source;

USE batch_etl_source;


-- Customer source table

CREATE TABLE IF NOT EXISTS customers (
    customer_id VARCHAR(20) PRIMARY KEY,
    customer_name VARCHAR(100) NOT NULL,
    email VARCHAR(150) NOT NULL,
    city VARCHAR(100),
    country VARCHAR(50),
    signup_date DATE
);


-- Order source table

CREATE TABLE IF NOT EXISTS orders (
    order_id VARCHAR(20) PRIMARY KEY,
    customer_id VARCHAR(20) NOT NULL,
    order_date DATE NOT NULL,
    product VARCHAR(150) NOT NULL,
    category VARCHAR(100),
    quantity INT NOT NULL,
    unit_price DECIMAL(12, 2) NOT NULL,
    order_status VARCHAR(30),

    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)
);
