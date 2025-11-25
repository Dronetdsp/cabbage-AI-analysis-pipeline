"""
Tests for CSV Data Loader
"""

import pytest
import pandas as pd
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.utils.csv_loader import CSVDataLoader, validate_csv_format


@pytest.fixture
def sample_csv(tmp_path):
    """Create a sample CSV file for testing"""
    csv_file = tmp_path / "test_images.csv"

    data = {
        'image_path': [
            'images/cabbage1.jpg',
            'images/cabbage2.jpg',
            'images/cabbage3.jpg'
        ],
        'label': ['healthy', 'diseased', 'healthy'],
        'field_id': [1, 1, 2]
    }

    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)

    return str(csv_file)


@pytest.fixture
def invalid_csv(tmp_path):
    """Create an invalid CSV file (missing image_path column)"""
    csv_file = tmp_path / "invalid.csv"

    data = {
        'filename': ['img1.jpg', 'img2.jpg'],
        'label': ['healthy', 'diseased']
    }

    df = pd.DataFrame(data)
    df.to_csv(csv_file, index=False)

    return str(csv_file)


class TestCSVDataLoader:
    """Test cases for CSVDataLoader class"""

    def test_load_valid_csv(self, sample_csv):
        """Test loading a valid CSV file"""
        loader = CSVDataLoader(sample_csv)
        data = loader.load()

        assert data is not None
        assert len(data) == 3
        assert 'image_path' in data.columns
        assert 'absolute_path' in data.columns

    def test_missing_csv_file(self):
        """Test error handling for missing CSV file"""
        loader = CSVDataLoader('nonexistent.csv')

        with pytest.raises(FileNotFoundError):
            loader.load()

    def test_invalid_csv_format(self, invalid_csv):
        """Test error handling for invalid CSV format"""
        loader = CSVDataLoader(invalid_csv)

        with pytest.raises(ValueError, match="must contain 'image_path' column"):
            loader.load()

    def test_get_summary(self, sample_csv):
        """Test getting summary statistics"""
        loader = CSVDataLoader(sample_csv)
        summary = loader.get_summary()

        assert 'total_records' in summary
        assert 'valid_images' in summary
        assert 'invalid_images' in summary
        assert summary['total_records'] == 3

    def test_validate_csv_format_valid(self, sample_csv):
        """Test validation of valid CSV format"""
        result = validate_csv_format(sample_csv)

        assert result['valid'] is True
        assert result['row_count'] == 3
        assert 'image_path' in result['columns']
        assert result['error'] is None

    def test_validate_csv_format_invalid(self, invalid_csv):
        """Test validation of invalid CSV format"""
        result = validate_csv_format(invalid_csv)

        assert result['valid'] is False
        assert result['error'] is not None

    def test_absolute_path_resolution(self, sample_csv, tmp_path):
        """Test resolution of relative to absolute paths"""
        loader = CSVDataLoader(sample_csv, base_path=str(tmp_path))
        data = loader.load()

        for path in data['absolute_path']:
            assert os.path.isabs(path)


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
