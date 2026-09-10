# Binary Intelligence  Analysis Platform for CI/CD piplines


## Objective
This platform provides automated binary intelligence and sandboxed analysis for DevSecOps workflows by receiving executable artifacts, performing static analysis, and returning structured JSON reports.







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


