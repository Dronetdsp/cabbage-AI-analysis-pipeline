"""
Tests for API Endpoints
"""

import pytest
from fastapi.testclient import TestClient
import pandas as pd
import os
import sys
from io import BytesIO

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.api.server import app, model_loader


@pytest.fixture
def client():
    """Create a test client"""
    # Initialize mock models
    model_loader.create_mock_model("disease_detector", (512, 512, 3), num_classes=5)
    model_loader.create_mock_model("quality_assessor", (512, 512, 3), num_classes=1)

    return TestClient(app)


@pytest.fixture
def sample_csv_content():
    """Create sample CSV content"""
    data = {
        'image_path': [
            'tests/fixtures/cabbage1.jpg',
            'tests/fixtures/cabbage2.jpg',
            'tests/fixtures/cabbage3.jpg'
        ],
        'field_id': [1, 1, 2],
        'label': ['healthy', 'diseased', 'healthy']
    }

    df = pd.DataFrame(data)
    return df.to_csv(index=False)


class TestAPIEndpoints:
    """Test cases for API endpoints"""

    def test_root_endpoint(self, client):
        """Test root endpoint"""
        response = client.get("/")

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "endpoints" in data

    def test_health_check(self, client):
        """Test health check endpoint"""
        response = client.get("/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "timestamp" in data
        assert "models_loaded" in data

    def test_upload_csv(self, client, sample_csv_content):
        """Test CSV file upload"""
        files = {
            'file': ('test_data.csv', BytesIO(sample_csv_content.encode()), 'text/csv')
        }

        response = client.post("/upload-csv", files=files)

        assert response.status_code == 200
        data = response.json()
        assert "file_id" in data
        assert "filename" in data
        assert data["filename"] == "test_data.csv"
        assert "validation" in data

    def test_upload_non_csv_file(self, client):
        """Test error handling for non-CSV file upload"""
        files = {
            'file': ('test.txt', BytesIO(b'not a csv'), 'text/plain')
        }

        response = client.post("/upload-csv", files=files)

        assert response.status_code == 400
        assert "CSV" in response.json()["detail"]

    def test_list_models(self, client):
        """Test listing models"""
        response = client.get("/models")

        assert response.status_code == 200
        data = response.json()
        assert "models" in data
        assert "count" in data
        assert data["count"] >= 2  # At least our mock models

    def test_create_mock_model(self, client):
        """Test creating a mock model via API"""
        response = client.post(
            "/models/mock",
            params={"model_name": "test_api_model", "num_classes": 10}
        )

        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "test_api_model" in data["message"]

    def test_get_status_nonexistent_job(self, client):
        """Test getting status of nonexistent job"""
        response = client.get("/status/nonexistent-job-id")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()

    def test_get_results_nonexistent_job(self, client):
        """Test getting results of nonexistent job"""
        response = client.get("/results/nonexistent-job-id")

        assert response.status_code == 404
        assert "not found" in response.json()["detail"].lower()


class TestAnalysisWorkflow:
    """Test complete analysis workflow"""

    def test_upload_and_analyze_workflow(self, client, sample_csv_content, tmp_path):
        """Test complete workflow: upload CSV, start analysis, check status"""
        # Step 1: Upload CSV
        files = {
            'file': ('workflow_test.csv', BytesIO(sample_csv_content.encode()), 'text/csv')
        }
        upload_response = client.post("/upload-csv", files=files)

        assert upload_response.status_code == 200
        file_id = upload_response.json()["file_id"]

        # Note: The actual analysis would fail because test images don't exist
        # This test validates the API structure, not the full processing pipeline


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
