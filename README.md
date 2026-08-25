# Automated Binary Intelligence Sandboxed Analysis Platform for DevSecOps

## Objective
This platform provides automated binary intelligence and sandboxed analysis for DevSecOps workflows by receiving executable artifacts, performing static analysis, and returning structured JSON reports.

## Architecture
- **API:** FastAPI
- **Worker:** Celery
- **Broker:** Redis
- **Database:** PostgreSQL

## Phase 1 Scope
- Secure file upload API
- Asynchronous task processing
- Static analysis: File type ID, PE/ELF metadata, YARA/capa integration
- Persistence in PostgreSQL

## Phase 2 Scope (Completed)
- Threat Intelligence (TI) enrichment for analyzed artifacts.
- Integration with (mock) TI providers.
- Asynchronous enrichment pipeline.
- Database schema extended for TI data.

## Prerequisites
- Docker
- Docker Compose

## How to start with Docker Compose
```bash
docker-compose up --build
```
*Note: After services start, run `docker compose exec api alembic upgrade head` to apply database migrations.*

## How to submit a file
```bash
curl -X POST -F "file=@/path/to/executable" http://localhost:8000/api/v1/analyze
```

## How to retrieve results
```bash
curl http://localhost:8000/api/v1/analysis/{analysis_id}
```

## Security Considerations
- No execution of binaries.
- No host filesystem mounts.
- Filesystem isolation via Docker volumes.
- Non-root containers.

