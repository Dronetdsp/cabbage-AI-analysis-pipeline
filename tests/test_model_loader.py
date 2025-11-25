"""
Tests for Model Loader
"""

import pytest
import numpy as np
import os
import sys
import json

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.models.model_loader import ModelLoader


@pytest.fixture
def model_loader(tmp_path):
    """Create a model loader instance"""
    return ModelLoader(model_dir=str(tmp_path))


@pytest.fixture
def model_config(tmp_path):
    """Create a sample model configuration file"""
    config_path = tmp_path / "models_config.json"

    config = {
        "models": {
            "test_model": {
                "path": "test_model.h5",
                "framework": "tensorflow"
            }
        }
    }

    with open(config_path, 'w') as f:
        json.dump(config, f)

    return str(config_path)


class TestModelLoader:
    """Test cases for ModelLoader class"""

    def test_initialization(self, tmp_path):
        """Test model loader initialization"""
        loader = ModelLoader(model_dir=str(tmp_path))

        assert loader.model_dir == str(tmp_path)
        assert len(loader.models) == 0
        assert len(loader.model_configs) == 0

    def test_create_mock_model(self, model_loader):
        """Test creating a mock model"""
        model_loader.create_mock_model(
            model_name="test_mock",
            input_shape=(512, 512, 3),
            num_classes=5
        )

        assert "test_mock" in model_loader.models
        assert "test_mock" in model_loader.model_configs

        config = model_loader.model_configs["test_mock"]
        assert config['framework'] == 'mock'
        assert config['input_shape'] == (None, 512, 512, 3)
        assert config['output_shape'] == (None, 5)

    def test_get_model(self, model_loader):
        """Test getting a loaded model"""
        model_loader.create_mock_model("test_model", (512, 512, 3))

        model = model_loader.get_model("test_model")
        assert model is not None

    def test_get_nonexistent_model(self, model_loader):
        """Test error handling for nonexistent model"""
        with pytest.raises(KeyError, match="Model 'nonexistent' not loaded"):
            model_loader.get_model("nonexistent")

    def test_predict_mock_model(self, model_loader):
        """Test prediction with mock model"""
        model_loader.create_mock_model("test_model", (512, 512, 3), num_classes=5)

        # Create test input
        test_input = np.random.rand(2, 512, 512, 3).astype(np.float32)

        # Run prediction
        predictions = model_loader.predict("test_model", test_input)

        assert predictions.shape == (2, 5)
        assert predictions.dtype in [np.float32, np.float64]

    def test_list_models(self, model_loader):
        """Test listing loaded models"""
        model_loader.create_mock_model("model1", (512, 512, 3))
        model_loader.create_mock_model("model2", (256, 256, 3))

        models = model_loader.list_models()

        assert len(models) == 2
        assert "model1" in models
        assert "model2" in models

    def test_unload_model(self, model_loader):
        """Test unloading a model"""
        model_loader.create_mock_model("test_model", (512, 512, 3))

        assert "test_model" in model_loader.models

        model_loader.unload_model("test_model")

        assert "test_model" not in model_loader.models
        assert "test_model" not in model_loader.model_configs

    def test_load_nonexistent_model_file(self, model_loader):
        """Test error handling for nonexistent model file"""
        with pytest.raises(FileNotFoundError):
            model_loader.load_model(
                model_name="test",
                model_path="nonexistent.h5",
                framework="tensorflow"
            )

    def test_unsupported_framework(self, model_loader, tmp_path):
        """Test error handling for unsupported framework"""
        # Create a dummy file
        model_file = tmp_path / "model.file"
        model_file.write_text("dummy")

        with pytest.raises(ValueError, match="Unsupported framework"):
            model_loader.load_model(
                model_name="test",
                model_path=str(model_file),
                framework="unsupported"
            )


class TestModelPrediction:
    """Test cases for model prediction functionality"""

    def test_batch_prediction(self, model_loader):
        """Test batch prediction"""
        model_loader.create_mock_model("test_model", (512, 512, 3), num_classes=3)

        # Create batch input
        batch_input = np.random.rand(5, 512, 512, 3).astype(np.float32)

        predictions = model_loader.predict("test_model", batch_input)

        assert predictions.shape[0] == 5
        assert predictions.shape[1] == 3

    def test_single_prediction(self, model_loader):
        """Test single image prediction"""
        model_loader.create_mock_model("test_model", (512, 512, 3), num_classes=10)

        # Create single input (still needs batch dimension)
        single_input = np.random.rand(1, 512, 512, 3).astype(np.float32)

        predictions = model_loader.predict("test_model", single_input)

        assert predictions.shape == (1, 10)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
