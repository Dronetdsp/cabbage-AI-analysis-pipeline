"""
FastAPI Server for Cabbage AI Analysis Pipeline
Provides REST API endpoints for image analysis via CSV upload
"""

from fastapi import FastAPI, File, UploadFile, HTTPException, BackgroundTasks
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import os
import sys
import shutil
from datetime import datetime
import uuid

# Add parent directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../..'))

from src.utils.csv_loader import CSVDataLoader, validate_csv_format
from src.preprocessing.image_preprocessor import ImagePreprocessor
from src.models.model_loader import ModelLoader


app = FastAPI(
    title="Cabbage AI Analysis Pipeline API",
    description="API for analyzing cabbage images using AI models",
    version="1.0.0"
)

# Global instances
preprocessor = ImagePreprocessor(target_size=(512, 512))
model_loader = ModelLoader(model_dir="data/models")

# Storage for analysis jobs
analysis_jobs = {}


class AnalysisRequest(BaseModel):
    """Request model for analysis"""
    csv_file_id: str
    base_path: Optional[str] = None
    models: Optional[List[str]] = ["disease_detector"]


class AnalysisResult(BaseModel):
    """Result model for analysis"""
    job_id: str
    status: str
    total_images: int
    processed_images: int
    results: Optional[List[Dict]] = None
    errors: Optional[List[Dict]] = None


@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Cabbage AI Analysis Pipeline API",
        "version": "1.0.0",
        "endpoints": {
            "upload_csv": "/upload-csv",
            "analyze": "/analyze",
            "status": "/status/{job_id}",
            "results": "/results/{job_id}",
            "models": "/models",
            "health": "/health"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "models_loaded": len(model_loader.list_models())
    }


@app.post("/upload-csv")
async def upload_csv(file: UploadFile = File(...)):
    """
    Upload a CSV file containing image paths for analysis

    CSV format required:
    - Must have 'image_path' column
    - Optional columns: 'id', 'metadata', etc.

    Returns:
        File ID and validation results
    """
    # Validate file extension
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="File must be a CSV file")

    # Generate unique file ID
    file_id = str(uuid.uuid4())
    upload_dir = "data/uploads"
    os.makedirs(upload_dir, exist_ok=True)

    # Save uploaded file
    file_path = os.path.join(upload_dir, f"{file_id}.csv")

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to save file: {str(e)}")

    # Validate CSV format
    validation = validate_csv_format(file_path)

    return {
        "file_id": file_id,
        "filename": file.filename,
        "validation": validation,
        "message": "CSV uploaded successfully" if validation['valid'] else "CSV validation failed"
    }


@app.post("/analyze")
async def start_analysis(
    file_id: str,
    base_path: Optional[str] = None,
    background_tasks: BackgroundTasks = None
):
    """
    Start analysis job for uploaded CSV file

    Args:
        file_id: ID of uploaded CSV file
        base_path: Base directory for resolving relative image paths

    Returns:
        Job ID and initial status
    """
    csv_path = os.path.join("data/uploads", f"{file_id}.csv")

    if not os.path.exists(csv_path):
        raise HTTPException(status_code=404, detail="CSV file not found")

    # Create job
    job_id = str(uuid.uuid4())

    try:
        # Load CSV
        loader = CSVDataLoader(csv_path, base_path)
        loader.load()
        summary = loader.get_summary()

        # Initialize job
        analysis_jobs[job_id] = {
            "job_id": job_id,
            "status": "queued",
            "csv_file_id": file_id,
            "total_images": summary['valid_images'],
            "processed_images": 0,
            "created_at": datetime.now().isoformat(),
            "results": [],
            "errors": []
        }

        # Start background processing
        if background_tasks:
            background_tasks.add_task(process_analysis_job, job_id, loader)
        else:
            # Synchronous processing for testing
            process_analysis_job(job_id, loader)

        return {
            "job_id": job_id,
            "status": "queued",
            "summary": summary,
            "message": f"Analysis started for {summary['valid_images']} images"
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start analysis: {str(e)}")


@app.get("/status/{job_id}")
async def get_status(job_id: str):
    """Get status of analysis job"""
    if job_id not in analysis_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = analysis_jobs[job_id]

    return {
        "job_id": job_id,
        "status": job['status'],
        "total_images": job['total_images'],
        "processed_images": job['processed_images'],
        "progress": f"{job['processed_images']}/{job['total_images']}"
    }


@app.get("/results/{job_id}")
async def get_results(job_id: str):
    """Get results of completed analysis job"""
    if job_id not in analysis_jobs:
        raise HTTPException(status_code=404, detail="Job not found")

    job = analysis_jobs[job_id]

    if job['status'] not in ['completed', 'completed_with_errors']:
        return {
            "job_id": job_id,
            "status": job['status'],
            "message": "Analysis not yet completed"
        }

    return {
        "job_id": job_id,
        "status": job['status'],
        "total_images": job['total_images'],
        "processed_images": job['processed_images'],
        "results": job['results'],
        "errors": job['errors']
    }


@app.get("/models")
async def list_models():
    """List all loaded models"""
    models = model_loader.list_models()

    return {
        "models": models,
        "count": len(models)
    }


@app.post("/models/load")
async def load_model(model_name: str, model_path: str, framework: str = "tensorflow"):
    """
    Load a new model

    Args:
        model_name: Name identifier for the model
        model_path: Path to model file
        framework: ML framework ('tensorflow' or 'pytorch')
    """
    try:
        model_loader.load_model(model_name, model_path, framework)
        return {
            "message": f"Model '{model_name}' loaded successfully",
            "config": model_loader.model_configs.get(model_name)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load model: {str(e)}")


@app.post("/models/mock")
async def create_mock_model(model_name: str, num_classes: int = 5):
    """Create a mock model for testing"""
    try:
        model_loader.create_mock_model(
            model_name=model_name,
            input_shape=(512, 512, 3),
            num_classes=num_classes
        )
        return {
            "message": f"Mock model '{model_name}' created successfully",
            "config": model_loader.model_configs.get(model_name)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create mock model: {str(e)}")


def process_analysis_job(job_id: str, loader: CSVDataLoader):
    """
    Background task to process analysis job

    Args:
        job_id: Job identifier
        loader: CSV data loader instance
    """
    job = analysis_jobs[job_id]
    job['status'] = 'processing'

    valid_images = loader.get_valid_images()

    for idx, record in enumerate(valid_images):
        try:
            image_path = record['absolute_path']

            # Preprocess image
            preprocessed = preprocessor.preprocess(image_path)

            # Get image stats
            stats = preprocessor.get_image_stats(preprocessed)

            # Mock analysis result (replace with actual model inference)
            result = {
                'image_path': record['image_path'],
                'preprocessed_shape': preprocessed.shape,
                'stats': stats,
                'analysis': {
                    'quality_score': 0.85,
                    'disease_detected': False,
                    'maturity': 'ready',
                    'estimated_weight': 1.5
                }
            }

            job['results'].append(result)
            job['processed_images'] = idx + 1

        except Exception as e:
            job['errors'].append({
                'image_path': record.get('image_path', 'unknown'),
                'error': str(e)
            })

    # Update final status
    if job['errors']:
        job['status'] = 'completed_with_errors'
    else:
        job['status'] = 'completed'


if __name__ == "__main__":
    import uvicorn

    # Create mock models for testing
    print("Creating mock models for testing...")
    model_loader.create_mock_model("disease_detector", (512, 512, 3), num_classes=5)
    model_loader.create_mock_model("quality_assessor", (512, 512, 3), num_classes=1)

    print("\n" + "=" * 60)
    print("Starting Cabbage AI Analysis Pipeline API Server")
    print("=" * 60)
    print("\nAPI Documentation: http://localhost:8000/docs")
    print("Alternative Documentation: http://localhost:8000/redoc")
    print("\n" + "=" * 60 + "\n")

    uvicorn.run(app, host="0.0.0.0", port=8000)
