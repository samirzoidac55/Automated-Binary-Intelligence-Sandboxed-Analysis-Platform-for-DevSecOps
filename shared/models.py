from sqlalchemy import create_engine, Column, String, Integer, DateTime, JSON, ForeignKey, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime
import enum
import os

DATABASE_URL = os.getenv("POSTGRES_URL", "postgresql://postgres:postgres_password@postgres:5432/binary_intelligence")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class JobStatus(enum.Enum):
    QUEUED = "QUEUED"
    RUNNING = "RUNNING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class Artifact(Base):
    __tablename__ = "artifacts"

    id = Column(String, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    sha256 = Column(String, nullable=False, index=True)
    size = Column(Integer, nullable=False)
    file_type = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    analyses = relationship("Analysis", back_populates="artifact")

class Analysis(Base):
    __tablename__ = "analyses"

    id = Column(String, primary_key=True, index=True)
    artifact_id = Column(String, ForeignKey("artifacts.id"), nullable=False)
    status = Column(Enum(JobStatus), default=JobStatus.QUEUED)
    error = Column(String)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    artifact = relationship("Artifact", back_populates="analyses")
    results = relationship("AnalysisResult", back_populates="analysis", uselist=False)

class AnalysisResult(Base):
    __tablename__ = "analysis_results"

    id = Column(Integer, primary_key=True, index=True)
    analysis_id = Column(String, ForeignKey("analyses.id"), nullable=False)
    results = Column(JSON)  # The structured JSON report
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    analysis = relationship("Analysis", back_populates="results")
