# Changelog

All notable changes to the Cabbage AI Analysis Pipeline project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-11-25

### Added
- **CSV Data Loader**: Load and validate image paths from CSV files
  - Automatic path resolution (relative to absolute)
  - File existence validation
  - Support for multiple metadata columns
  - Summary statistics and reporting

- **Image Preprocessor**: Complete image preprocessing pipeline
  - Image loading and validation
  - Resizing to target dimensions
  - Normalization (0-1 range)
  - Color correction using CLAHE
  - Background removal with color thresholding
  - Data augmentation (flip, rotate, brightness)
  - Image statistics extraction

- **Model Loader**: Flexible AI model management
  - TensorFlow/Keras model support
  - PyTorch model support
  - Mock model creation for testing
  - Batch prediction capabilities
  - Model configuration management
  - Config-based model loading

- **REST API Server**: FastAPI-based API endpoints
  - CSV file upload endpoint
  - Analysis job creation and management
  - Job status tracking
  - Result retrieval
  - Model management endpoints
  - Health check endpoint
  - Interactive API documentation (Swagger UI)

- **Testing Suite**: Comprehensive test coverage
  - CSV loader unit tests
  - Image preprocessor unit tests
  - Model loader unit tests
  - API integration tests
  - pytest configuration
  - Test fixtures and utilities

- **Documentation**:
  - QUICKSTART.md: Quick start guide in Korean
  - TESTING_GUIDE.md: Comprehensive testing guide in Korean
  - cabbage-AI-analysis-pipeline.md: Full system documentation
  - README.md: Project overview and getting started
  - Sample CSV template

- **Project Structure**:
  - Organized source code in `src/` directory
  - Separate test directory with comprehensive tests
  - Data directories for input, output, and uploads
  - Python package structure with `__init__.py` files

### Features
- Batch processing of images via CSV upload
- Real-time job status tracking
- Background task processing
- Extensible model architecture
- RESTful API design
- Complete error handling and validation

### Technical Details
- Python 3.8+ compatibility
- OpenCV for image processing
- NumPy and Pandas for data handling
- FastAPI for REST API
- pytest for testing
- Support for both TensorFlow and PyTorch

[1.0.0]: https://github.com/Dronetdsp/cabbage-AI-analysis-pipeline/releases/tag/v1.0.0
