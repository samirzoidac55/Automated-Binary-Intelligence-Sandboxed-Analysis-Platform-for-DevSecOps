from shared.celery_app import celery_app
from shared.models import SessionLocal, Analysis, AnalysisResult, JobStatus
from analysis.engine import static_analysis_engine
import os
import logging

logger = logging.getLogger(__name__)

@celery_app.task(name="analysis.tasks.static_analysis")
def static_analysis(analysis_id: str, file_path: str):
    db = SessionLocal()
    try:
        # Update status to RUNNING
        db_analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if not db_analysis:
            logger.error(f"Analysis {analysis_id} not found")
            return
        
        db_analysis.status = JobStatus.RUNNING
        db.commit()
        
        # Perform analysis
        file_type = db_analysis.artifact.file_type
        results = static_analysis_engine(file_path, file_type)
        
        # Save results
        db_result = AnalysisResult(
            analysis_id=analysis_id,
            results=results
        )
        db.add(db_result)
        
        # Update status to COMPLETED
        db_analysis.status = JobStatus.COMPLETED
        db.commit()
        
    except Exception as e:
        logger.error(f"Error processing analysis {analysis_id}: {e}")
        db_analysis = db.query(Analysis).filter(Analysis.id == analysis_id).first()
        if db_analysis:
            db_analysis.status = JobStatus.FAILED
            db_analysis.error = str(e)
            db.commit()
    finally:
        # Cleanup: Remove file after analysis
        if os.path.exists(file_path):
            os.remove(file_path)
        db.close()
