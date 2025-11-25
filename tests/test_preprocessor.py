"""
Tests for Image Preprocessor
"""

import pytest
import numpy as np
import os
import sys
from PIL import Image

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.preprocessing.image_preprocessor import ImagePreprocessor


@pytest.fixture
def sample_image(tmp_path):
    """Create a sample test image"""
    img_path = tmp_path / "test_image.jpg"

    # Create a simple RGB image
    img_array = np.random.randint(0, 255, (600, 800, 3), dtype=np.uint8)
    img = Image.fromarray(img_array)
    img.save(img_path)

    return str(img_path)


@pytest.fixture
def preprocessor():
    """Create a preprocessor instance"""
    return ImagePreprocessor(target_size=(512, 512), normalize=True)


class TestImagePreprocessor:
    """Test cases for ImagePreprocessor class"""

    def test_initialization(self):
        """Test preprocessor initialization"""
        preprocessor = ImagePreprocessor(target_size=(256, 256), normalize=False)

        assert preprocessor.target_size == (256, 256)
        assert preprocessor.normalize is False
        assert preprocessor.color_mode == 'RGB'

    def test_load_image(self, preprocessor, sample_image):
        """Test loading an image"""
        image = preprocessor.load_image(sample_image)

        assert isinstance(image, np.ndarray)
        assert len(image.shape) == 3
        assert image.shape[2] == 3  # RGB channels

    def test_load_nonexistent_image(self, preprocessor):
        """Test error handling for nonexistent image"""
        with pytest.raises(FileNotFoundError):
            preprocessor.load_image('nonexistent.jpg')

    def test_resize_image(self, preprocessor):
        """Test image resizing"""
        # Create a test image
        image = np.random.randint(0, 255, (600, 800, 3), dtype=np.uint8)
        resized = preprocessor.resize_image(image)

        assert resized.shape == (512, 512, 3)

    def test_normalize_image(self, preprocessor):
        """Test image normalization"""
        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        normalized = preprocessor.normalize_image(image)

        assert normalized.dtype == np.float32
        assert normalized.min() >= 0.0
        assert normalized.max() <= 1.0

    def test_preprocess_pipeline(self, preprocessor, sample_image):
        """Test complete preprocessing pipeline"""
        preprocessed = preprocessor.preprocess(sample_image)

        assert preprocessed.shape == (512, 512, 3)
        assert preprocessed.dtype == np.float32
        assert preprocessed.min() >= 0.0
        assert preprocessed.max() <= 1.0

    def test_preprocess_batch(self, preprocessor, tmp_path):
        """Test batch preprocessing"""
        # Create multiple test images
        image_paths = []
        for i in range(3):
            img_path = tmp_path / f"test_image_{i}.jpg"
            img_array = np.random.randint(0, 255, (600, 800, 3), dtype=np.uint8)
            img = Image.fromarray(img_array)
            img.save(img_path)
            image_paths.append(str(img_path))

        batch = preprocessor.preprocess_batch(image_paths)

        assert batch.shape == (3, 512, 512, 3)
        assert batch.dtype == np.float32

    def test_get_image_stats(self, preprocessor):
        """Test getting image statistics"""
        image = np.random.rand(512, 512, 3).astype(np.float32)
        stats = preprocessor.get_image_stats(image)

        assert 'shape' in stats
        assert 'dtype' in stats
        assert 'min' in stats
        assert 'max' in stats
        assert 'mean' in stats
        assert 'std' in stats

    def test_augment_image_flip(self, preprocessor):
        """Test horizontal flip augmentation"""
        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        augmented = preprocessor.augment_image(image, flip_horizontal=True)

        assert augmented.shape == image.shape
        assert not np.array_equal(augmented, image)

    def test_augment_image_rotate(self, preprocessor):
        """Test rotation augmentation"""
        image = np.random.randint(0, 255, (512, 512, 3), dtype=np.uint8)
        augmented = preprocessor.augment_image(image, rotate_angle=45)

        assert augmented.shape == image.shape

    def test_augment_image_brightness(self, preprocessor):
        """Test brightness augmentation"""
        image = np.random.randint(100, 150, (512, 512, 3), dtype=np.uint8)
        augmented = preprocessor.augment_image(image, brightness_factor=1.5)

        assert augmented.shape == image.shape
        assert augmented.mean() > image.mean()


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
