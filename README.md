# Retail Lakehouse Platform

## Overview

An end-to-end Retail Analytics Platform built using Databricks Free Edition implementing Medallion Architecture (Bronze, Silver, Gold).

## Architecture

Source Systems
→ Validation
→ Bronze Layer
→ Silver Layer
→ Gold Layer
→ Audit Framework
→ Dashboard

## Technology Stack

- Databricks
- PySpark
- SQL
- Delta Tables
- GitHub

## Features

- Source Data Generation
- Data Validation Framework
- Bronze Layer Ingestion
- Silver Layer Transformation
- Gold Layer KPI Aggregation
- Audit & Monitoring
- Executive Dashboard

## Layers

### Source
orders_source
customers_source
products_source
returns_source

### Bronze
Raw business data with metadata.

### Silver
Validated and cleaned business data.

### Gold
Business KPIs and reporting tables.

### Audit
Pipeline monitoring and record count tracking.

## Dashboard

- Total Revenue
- Total Profit
- Total Customers
- Total Orders
- Top Customers
- Top Products
- Category Performance

## Project Outcome

Built a production-style Lakehouse architecture demonstrating data engineering, auditing, reporting, and data modeling concepts using Databricks.
