"""
Model Loader for Cabbage AI Analysis Pipeline
Handles loading and managing AI models for inference
"""

import os
import json
from typing import Dict, Optional, Any
import numpy as np


class ModelLoader:
    """Load and manage AI models for cabbage analysis"""

    def __init__(self, model_dir: str = "data/models"):
        """
        Initialize model loader

        Args:
            model_dir: Directory containing model files
        """
        self.model_dir = model_dir
        self.models = {}
        self.model_configs = {}

    def load_model(self, model_name: str, model_path: str, framework: str = "tensorflow") -> Any:
        """
        Load a model from file

        Args:
            model_name: Name identifier for the model
            model_path: Path to model file
            framework: ML framework ('tensorflow' or 'pytorch')

        Returns:
            Loaded model object

        Raises:
            FileNotFoundError: If model file doesn't exist
            ValueError: If framework is not supported
        """
        full_path = os.path.join(self.model_dir, model_path) if not os.path.isabs(model_path) else model_path

        if not os.path.exists(full_path):
            raise FileNotFoundError(f"Model file not found: {full_path}")

        if framework == "tensorflow":
            return self._load_tensorflow_model(model_name, full_path)
        elif framework == "pytorch":
            return self._load_pytorch_model(model_name, full_path)
        else:
            raise ValueError(f"Unsupported framework: {framework}")

    def _load_tensorflow_model(self, model_name: str, model_path: str) -> Any:
        """
        Load TensorFlow/Keras model

        Args:
            model_name: Name identifier for the model
            model_path: Path to model file

        Returns:
            Loaded TensorFlow model
        """
        try:
            import tensorflow as tf

            model = tf.keras.models.load_model(model_path)
            self.models[model_name] = model

            # Store model config
            self.model_configs[model_name] = {
                'framework': 'tensorflow',
                'path': model_path,
                'input_shape': model.input_shape,
                'output_shape': model.output_shape
            }

            print(f"✓ Loaded TensorFlow model '{model_name}' from {model_path}")
            return model

        except ImportError:
            raise ImportError("TensorFlow is not installed. Install with: pip install tensorflow")
        except Exception as e:
            raise RuntimeError(f"Failed to load TensorFlow model: {e}")

    def _load_pytorch_model(self, model_name: str, model_path: str) -> Any:
        """
        Load PyTorch model

        Args:
            model_name: Name identifier for the model
            model_path: Path to model file

        Returns:
            Loaded PyTorch model
        """
        try:
            import torch

            model = torch.load(model_path)
            model.eval()  # Set to evaluation mode
            self.models[model_name] = model

            # Store model config
            self.model_configs[model_name] = {
                'framework': 'pytorch',
                'path': model_path,
            }

            print(f"✓ Loaded PyTorch model '{model_name}' from {model_path}")
            return model

        except ImportError:
            raise ImportError("PyTorch is not installed. Install with: pip install torch")
        except Exception as e:
            raise RuntimeError(f"Failed to load PyTorch model: {e}")

    def get_model(self, model_name: str) -> Any:
        """
        Get a loaded model by name

        Args:
            model_name: Name identifier for the model

        Returns:
            Model object

        Raises:
            KeyError: If model is not loaded
        """
        if model_name not in self.models:
            raise KeyError(f"Model '{model_name}' not loaded. Available models: {list(self.models.keys())}")

        return self.models[model_name]

    def predict(self, model_name: str, input_data: np.ndarray) -> np.ndarray:
        """
        Run prediction using a loaded model

        Args:
            model_name: Name identifier for the model
            input_data: Input data array

        Returns:
            Model predictions

        Raises:
            KeyError: If model is not loaded
        """
        model = self.get_model(model_name)
        config = self.model_configs[model_name]

        if config['framework'] == 'tensorflow':
            return self._predict_tensorflow(model, input_data)
        elif config['framework'] == 'pytorch':
            return self._predict_pytorch(model, input_data)

    def _predict_tensorflow(self, model: Any, input_data: np.ndarray) -> np.ndarray:
        """
        Run TensorFlow model prediction

        Args:
            model: TensorFlow model
            input_data: Input array

        Returns:
            Predictions
        """
        predictions = model.predict(input_data)
        return predictions

    def _predict_pytorch(self, model: Any, input_data: np.ndarray) -> np.ndarray:
        """
        Run PyTorch model prediction

        Args:
            model: PyTorch model
            input_data: Input array

        Returns:
            Predictions
        """
        import torch

        # Convert to tensor
        input_tensor = torch.from_numpy(input_data).float()

        # Run inference
        with torch.no_grad():
            predictions = model(input_tensor)

        # Convert back to numpy
        return predictions.cpu().numpy()

    def load_from_config(self, config_path: str) -> None:
        """
        Load multiple models from a configuration file

        Args:
            config_path: Path to JSON config file

        Config file format:
        {
            "models": {
                "disease_detector": {
                    "path": "disease_model.h5",
                    "framework": "tensorflow"
                },
                "quality_assessor": {
                    "path": "quality_model.pth",
                    "framework": "pytorch"
                }
            }
        }
        """
        if not os.path.exists(config_path):
            raise FileNotFoundError(f"Config file not found: {config_path}")

        with open(config_path, 'r') as f:
            config = json.load(f)

        if 'models' not in config:
            raise ValueError("Config file must contain 'models' key")

        for model_name, model_info in config['models'].items():
            try:
                self.load_model(
                    model_name=model_name,
                    model_path=model_info['path'],
                    framework=model_info.get('framework', 'tensorflow')
                )
            except Exception as e:
                print(f"✗ Failed to load model '{model_name}': {e}")

    def list_models(self) -> Dict[str, Dict]:
        """
        List all loaded models and their configurations

        Returns:
            Dictionary of model configurations
        """
        return self.model_configs.copy()

    def unload_model(self, model_name: str) -> None:
        """
        Unload a model from memory

        Args:
            model_name: Name identifier for the model
        """
        if model_name in self.models:
            del self.models[model_name]
            del self.model_configs[model_name]
            print(f"✓ Unloaded model '{model_name}'")
        else:
            print(f"Model '{model_name}' not found")

    def create_mock_model(self, model_name: str, input_shape: tuple, num_classes: int = 5) -> None:
        """
        Create a mock model for testing purposes

        Args:
            model_name: Name identifier for the model
            input_shape: Expected input shape (H, W, C)
            num_classes: Number of output classes
        """
        class MockModel:
            def __init__(self, input_shape, num_classes):
                self.input_shape = (None,) + input_shape
                self.output_shape = (None, num_classes)
                self.num_classes = num_classes

            def predict(self, x):
                batch_size = x.shape[0]
                # Return random predictions
                return np.random.rand(batch_size, self.num_classes)

        mock_model = MockModel(input_shape, num_classes)
        self.models[model_name] = mock_model
        self.model_configs[model_name] = {
            'framework': 'mock',
            'path': 'mock_model',
            'input_shape': mock_model.input_shape,
            'output_shape': mock_model.output_shape
        }

        print(f"✓ Created mock model '{model_name}'")
