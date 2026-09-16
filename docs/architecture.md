# Retail Lakehouse Platform Architecture

## Objective

Build a Retail Analytics Platform using Databricks and Delta Lake that provides business insights on sales, customers, products, and profitability.

## High-Level Architecture

```text
Source Systems
(Orders, Customers, Products, Returns)
                │
                ▼
      Data Validation Layer
      - Schema Validation
      - Null Checks
      - Duplicate Checks
                │
                ▼
         Bronze Layer
        (Raw Data Store)
                │
                ▼
         Silver Layer
    (Cleaned & Standardized)
                │
                ▼
          Gold Layer
      (Business KPI Tables)
                │
                ▼
      SQL Analytics & Dashboard
```

## Technology Stack

- Databricks Free Edition
- PySpark
- SQL
- Delta Lake
- GitHub

## Architecture Pattern

Medallion Architecture

Bronze → Silver → Gold
