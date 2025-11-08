# Elasticsearch Usage – Finance RAG

## 🔍 Business Search

- **Indexes**: `finance-rag-*`, `documents-*`
- **Source**: Manual ingestion or NLP pipelines
- **Query types**: Full-text search, vector similarity, structured filters
- **Purpose**: Powering lexical and semantic search for business-relevant content

## 📊 Logging and Observability

- **Indexes**: `logs-*`
- **Source**: Fluentd (Docker logs, application logs)
- **Retention**: 7 days (subject to rotation policy)
- **Format**: Raw JSON events
- **Purpose**: Infrastructure observability, debugging, and audit trails

## 🧠 Conventions and Safeguards

- Logs must never be ingested into business search indexes
- Kibana dashboards must only query `logs-*` indexes for observability
- NLP pipelines must explicitly exclude `logs-*` from ingestion or analysis
- Index naming must follow the pattern:
  - `logs-<source>-<date>` for logs (e.g., `logs-fluentd-2025.11.08`)
  - `finance-rag-<domain>` for business data (e.g., `finance-rag-contracts`)
- Index templates and ILM policies should be defined separately for logs and business data

## 📁 File Location

This file: `observability_config/elasticsearch_usage.md`
Maintainer: Abdias Arsène
Last updated: 2025-11-08
