from fastapi import FastAPI, UploadFile, File, Depends, HTTPException
from sqlalchemy.orm import Session
import uuid
import os
from shared.models import SessionLocal, Artifact, Analysis, JobStatus, AnalysisResult
from shared.schemas import AnalysisStatus, AnalysisResultSchema
from api.utils import calculate_sha256, save_upload_file, get_file_type
from shared.celery_app import celery_app

app = FastAPI(title="Binary Intelligence API", version="1.0.0")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/api/v1/health")
def health_check():
    return {"status": "healthy"}

@app.post("/api/v1/analyze")
async def analyze_file(file: UploadFile = File(...), db: Session = Depends(get_db)):
    artifact_id = str(uuid.uuid4())
    analysis_id = str(uuid.uuid4())
    
    upload_dir = os.getenv("UPLOAD_DIR", "/tmp/uploads")
    file_path = os.path.join(upload_dir, artifact_id)
    
    await save_upload_file(file, file_path)
    
    sha256 = calculate_sha256(file_path)
    file_size = os.path.getsize(file_path)
    file_type = get_file_type(file_path)
    
    # Store artifact metadata
    db_artifact = Artifact(
        id=artifact_id,
        filename=file.filename,
        sha256=sha256,
        size=file_size,
        file_type=file_type
    )
    db.add(db_artifact)
    
    # Create analysis job
    db_analysis = Analysis(
        id=analysis_id,
        artifact_id=artifact_id,
        status=JobStatus.QUEUED
    )
    db.add(db_analysis)
    db.commit()
    
    # Enqueue task
    celery_app.send_task("analysis.tasks.static_analysis", args=[analysis_id, file_path])
    
    return {"analysis_id": analysis_id, "artifact_id": artifact_id}

@app.get("/api/v1/analysis/{analysis_id}", response_model=AnalysisResultSchema)
def get_analysis(analysis_id: str, db: Session = Depends(get_db)):
    db_analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
    if not db_analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    db_result = db.query(AnalysisResult).filter(AnalysisResult.analysis_id == analysis_id).first()
    
    # If completed, return full results, otherwise return status
    return {
        "analysis_id": db_analysis.id,
        "artifact": {
            "filename": db_analysis.artifact.filename,
            "sha256": db_analysis.artifact.sha256,
            "size": db_analysis.artifact.size,
            "file_type": db_analysis.artifact.file_type
        },
        "static_analysis": db_result.results if db_result else {},
        "status": db_analysis.status,
        "created_at": db_analysis.created_at
    }
