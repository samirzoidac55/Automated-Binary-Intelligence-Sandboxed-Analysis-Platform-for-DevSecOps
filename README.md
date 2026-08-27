# Binary Intelligence Sandboxed Analysis Platform for DevSecOps pfa intership


## Objective
This platform provides automated binary intelligence and sandboxed analysis for DevSecOps workflows by receiving executable artifacts, performing static analysis, and returning structured JSON reports.



## Phase 1 Scope
- Secure file upload API
- Asynchronous task processing
- Static analysis: File type ID, PE/ELF metadata, YARA/capa integration
- Persistence in PostgreSQL




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


