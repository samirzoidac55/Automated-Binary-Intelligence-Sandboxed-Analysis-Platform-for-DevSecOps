from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime
from shared.models import JobStatus

class ArtifactBase(BaseModel):
    filename: str
    sha256: str
    size: int
    file_type: Optional[str] = None

class AnalysisCreate(BaseModel):
    artifact_id: str

class AnalysisStatus(BaseModel):
    analysis_id: str
    status: JobStatus
    error: Optional[str] = None
    created_at: datetime
    updated_at: datetime

class AnalysisResultSchema(BaseModel):
    analysis_id: str
    artifact: ArtifactBase
    static_analysis: Dict[str, Any]
    status: JobStatus
    created_at: datetime
