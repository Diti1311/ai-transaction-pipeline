# AI Transaction Processing Pipeline

A production-style backend pipeline that processes transaction CSV files asynchronously using FastAPI, Celery, Redis, PostgreSQL and Gemini AI.

## Features

* CSV Upload API
* Background Processing with Celery
* Data Cleaning

  * Date normalization
  * Amount normalization
  * Status normalization
  * Duplicate removal
* Anomaly Detection

  * Amount > 3x account median
  * USD used with domestic-only merchants (Swiggy, Ola, IRCTC)
* AI Merchant Categorization using Gemini
* AI Summary Generation
* Job Tracking
* Dockerized Deployment

---

## Tech Stack

* FastAPI
* PostgreSQL
* Redis
* Celery
* SQLAlchemy
* Pandas
* Gemini API
* Docker Compose

---

## Architecture

Client → FastAPI → PostgreSQL

Client → FastAPI → Redis Queue → Celery Worker

Celery Worker → CSV Processing → PostgreSQL

Celery Worker → Gemini AI → PostgreSQL

---

## Setup

Clone Repository

```bash
git clone <repo-url>
cd ai-transaction-pipeline
```

Create .env

```env
DATABASE_URL=postgresql://postgres:postgres@db:5432/transactions_db

REDIS_URL=redis://redis:6379/0

GEMINI_API_KEY=
```

Run

```bash
docker compose up --build
```

Swagger

```text
http://localhost:8000/docs
```

---

## Example Requests

Upload CSV

```bash
curl -X POST "http://localhost:8000/jobs/upload" \
-F "file=@transactions.csv"
```

Get Status

```bash
curl "http://localhost:8000/jobs/1/status"
```

Get Results

```bash
curl "http://localhost:8000/jobs/1/results"
```

List Jobs

```bash
curl "http://localhost:8000/jobs"
```

---

## Gemini Fallback

The application works even when GEMINI_API_KEY is not provided.

Fallback behavior:

* Merchant category → Other
* Summary → deterministic fallback summary
* Processing continues successfully

---

## Future Improvements

* Horizontal worker scaling
* Kafka-based queue
* S3 file storage
* Advanced anomaly detection models
* Prometheus/Grafana monitoring
* Authentication & RBAC
