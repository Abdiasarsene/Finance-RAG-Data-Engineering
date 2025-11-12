# Finance RAG : 01 - Data Engineering

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Docker](https://img.shields.io/badge/Docker-Containerized-informational?logo=docker)
![RabbitMQ](https://img.shields.io/badge/RabbitMQ-Message%20Queue-ff6600?logo=rabbitmq)
![MinIO](https://img.shields.io/badge/MinIO-Object%20Storage-e76f51?logo=minio)
![Prometheus](https://img.shields.io/badge/Prometheus-Monitoring-orange?logo=prometheus)
![Elasticsearch](https://img.shields.io/badge/Elasticsearch-Search%20Engine-005571?logo=elasticsearch)
![Kibana](https://img.shields.io/badge/Kibana-Observability-a600ff?logo=kibana)
![Fluentd](https://img.shields.io/badge/Fluentd-Logs%20Collector-0e83c8?logo=fluentd)
![Grafana](https://img.shields.io/badge/Grafana-Dashboards-F29F05?logo=grafana)

"*This repository provides the full Data Engineering backbone of a finance-domain RAG solution, ensuring that data entering the GenAI pipeline is clean, structured, observable, and production-ready. It delivers an end-to-end flow from ingestion through chunking to embeddings, implemented with distributed processing, centralized monitoring, and scalable storage. This module is intentionally focused on the data foundation, while the Retrieval, LLM orchestration, Serving API, and LLMOps components will be introduced in subsequent repositories as part of the complete multi-module architecture.*"

---

---

## 🧱 Core Capabilities

* Automated ingestion
* Document segmentation & embedding generation
* Distributed workers orchestrated via **RabbitMQ**
* Storage-agnostic design with **MinIO** backend
* Centralized logging & monitoring stack
* Integration tests for production-grade reliability
* Fully containerized architecture ready for CI/CD pipelines

---

---

## 🔃Data Pipeline Overview

Extraction & Storage – Raw data is collected from PDFs, URLs, and APIs, transformed into a unified JSON schema, and stored in MinIO. A dedicated worker (extract_worker.py) orchestrates message reception, applies domain-specific extractors, and publishes results. Structured logging and Prometheus metrics provide full traceability, observability, and scalability.

Processing, Chunking & Embedding – Texts are cleaned, deduplicated, language-detected, and format-validated by dedicated modules. Long texts are split into context-preserving chunks (by sentence, paragraph, or token) with overlaps and annotated with metadata. Chunks are then converted into semantic embeddings and stored in Milvus for fast retrieval. Orchestration (queues, retries, logs) remains fully decoupled from business logic, ensuring modular, reliable, and AI-ready data.

---

---

## 🏗️ Architecture Snapshot

![Roadmap Data Engineering](./statics/engineering.png)

---

---

## 🌐 Tech Stack

| Layer         | Tools                         |
| ------------- | ----------------------------- |
| Orchestration | RabbitMQ                      |
| Storage       | MinIO                         |
| Processing    | Python Workers                |
| Observability | Centralized logging & metrics |
| Runtime       | Docker & Compose              |

---

---

## 🚀 What’s Next

* **[Finance-RAG-Retriever-Layer](https://github.com/Abdiasarsene/Finance-RAG-Retriever-Layer)**
* **[Finance-RAG-LLM-Integration](https://github.com/Abdiasarsene/Finance-RAG-LLM-Integration)**
* **Finance-RAG-Agents**
* **Finance-RAG-Serving-API**
* **Finance-RAG-LLMops**
