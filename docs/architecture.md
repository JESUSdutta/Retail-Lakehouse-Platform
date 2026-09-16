# Retail Lakehouse Platform Architecture

## Objective

Build a Retail Analytics Platform using Databricks and Delta Lake that provides business insights on sales, customers, products, and profitability.

---

## High-Level Architecture

                    RETAIL ANALYTICS PLATFORM

┌─────────────────┐
│   Source Data   │
│                 │
│ orders.csv      │
│ customers.csv   │
│ products.csv    │
│ returns.csv     │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Data Validation │
│                 │
│ Schema Checks   │
│ Null Checks     │
│ Duplicate Check │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Bronze Layer    │
│ Raw Delta Data  │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Silver Layer    │
│ Cleaned Data    │
│ Standardized    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Gold Layer      │
│ KPI Tables      │
│ Aggregations    │
└────────┬────────┘
         │
         ▼
┌─────────────────┐
│ Dashboards      │
│ SQL Analytics   │
└─────────────────┘

---

## Technology Stack

- Databricks Free Edition
- PySpark
- SQL
- Delta Lake
- GitHub

---

## Architecture Pattern

Medallion Architecture

Bronze → Silver → Gold
