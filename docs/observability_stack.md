# 🛰️ Observability Stack – Finance RAG

This document formalizes the architecture, purpose, and persistence strategy of the observability and core service stacks. It ensures operational clarity, onboarding efficiency, and production readiness.

---

## 🧩 Stack Separation

| Stack               | File                                  | Purpose                                           |
| ------------------- | ------------------------------------- | ------------------------------------------------- |
| Core Services       | `docker-compose.stack.yaml`         | Business logic: vector search, storage, messaging |
| Observability Layer | `docker-compose.observability.yaml` | Monitoring, logging, metrics, dashboards          |

---

## 📦 Services Overview

### 🔹 Core Stack (`docker-compose.stack.yaml`)

| Service              | Container Name     | Port(s)     | Purpose                             | Volume(s)                  |
| -------------------- | ------------------ | ----------- | ----------------------------------- | -------------------------- |
| Milvus               | `milvus`         | 19530, 9091 | Vector database for semantic search | `milvus_data` (optional) |
| MinIO                | `minio`          | 9000        | S3-compatible object storage        | `minio_data`             |
| RabbitMQ             | `rabbitmq`       | 5672, 15672 | Messaging queue                     | `rabbitmq_data`          |
| Elasticsearch Search | `elastic_search` | 9202        | Business search engine              | `elastic_search_data`    |

### 🔸 Observability Stack (`docker-compose.observability.yaml`)

| Service            | Container Name               | Port(s)    | Purpose            | Volume(s)             |
| ------------------ | ---------------------------- | ---------- | ------------------ | --------------------- |
| Prometheus         | `prometheus_finance_rag`   | 9090       | Metrics collection | `prometheus_data`   |
| Grafana            | `grafana`                  | 3001→3000 | Metrics dashboards | (default)             |
| Fluentd            | `finance-rag-de-fluentd-1` | 24224      | Log collection     | (default)             |
| Elasticsearch Logs | `elastic_logs`             | 9201       | Log indexing       | `elastic_logs_data` |
| Kibana             | `finance-rag-de-kibana-1`  | 5601       | Log dashboards     | (default)             |
