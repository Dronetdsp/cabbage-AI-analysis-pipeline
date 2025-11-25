"""
CSV Data Loader for Cabbage AI Analysis Pipeline
Loads image paths and metadata from CSV files for batch processing
"""

import pandas as pd
import os
from typing import List, Dict, Optional
from pathlib import Path


class CSVDataLoader:
    """Load and validate image data from CSV files"""

    def __init__(self, csv_path: str, base_path: Optional[str] = None):
        """
        Initialize CSV data loader

        Args:
            csv_path: Path to CSV file
            base_path: Base directory for resolving relative image paths
        """
        self.csv_path = csv_path
        self.base_path = base_path or os.getcwd()
        self.data = None
        self.valid_extensions = {'.jpg', '.jpeg', '.png', '.bmp', '.tiff'}

    def load(self) -> pd.DataFrame:
        """
        Load CSV file and validate required columns

        Returns:
            DataFrame with validated data

        Raises:
            FileNotFoundError: If CSV file doesn't exist
            ValueError: If required columns are missing
        """
        if not os.path.exists(self.csv_path):
            raise FileNotFoundError(f"CSV file not found: {self.csv_path}")

        # Load CSV
        self.data = pd.read_csv(self.csv_path)

        # Validate required columns
        if 'image_path' not in self.data.columns:
            raise ValueError("CSV must contain 'image_path' column")

        # Resolve relative paths
        self.data['absolute_path'] = self.data['image_path'].apply(
            lambda x: os.path.join(self.base_path, x) if not os.path.isabs(x) else x
        )

        # Validate image paths
        self.data['exists'] = self.data['absolute_path'].apply(os.path.exists)
        self.data['valid_extension'] = self.data['absolute_path'].apply(
            lambda x: Path(x).suffix.lower() in self.valid_extensions
        )

        return self.data

    def get_valid_images(self) -> List[Dict]:
        """
        Get list of valid image records

        Returns:
            List of dictionaries containing image info
        """
        if self.data is None:
            self.load()

        valid_data = self.data[self.data['exists'] & self.data['valid_extension']]

        return valid_data.to_dict('records')

    def get_invalid_images(self) -> List[Dict]:
        """
        Get list of invalid image records

        Returns:
            List of dictionaries containing invalid image info
        """
        if self.data is None:
            self.load()

        invalid_data = self.data[~(self.data['exists'] & self.data['valid_extension'])]

        return invalid_data.to_dict('records')

    def get_summary(self) -> Dict:
        """
        Get summary statistics of the dataset

        Returns:
            Dictionary with summary information
        """
        if self.data is None:
            self.load()

        valid_count = (self.data['exists'] & self.data['valid_extension']).sum()

        summary = {
            'total_records': len(self.data),
            'valid_images': int(valid_count),
            'invalid_images': len(self.data) - int(valid_count),
            'missing_files': int((~self.data['exists']).sum()),
            'invalid_extensions': int((~self.data['valid_extension']).sum()),
            'columns': list(self.data.columns)
        }

        return summary


def validate_csv_format(csv_path: str) -> Dict:
    """
    Validate CSV file format without loading images

    Args:
        csv_path: Path to CSV file

    Returns:
        Validation results dictionary
    """
    try:
        df = pd.read_csv(csv_path)

        has_image_path = 'image_path' in df.columns

        return {
            'valid': has_image_path,
            'columns': list(df.columns),
            'row_count': len(df),
            'error': None if has_image_path else "Missing required 'image_path' column"
        }
    except Exception as e:
        return {
            'valid': False,
            'columns': [],
            'row_count': 0,
            'error': str(e)
        }
