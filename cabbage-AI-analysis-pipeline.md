# Cabbage AI Analysis Pipeline

## Overview

The Cabbage AI Analysis Pipeline is an end-to-end machine learning system designed to analyze cabbage crops using computer vision and AI techniques. This pipeline enables automated quality assessment, disease detection, growth monitoring, and yield prediction for cabbage cultivation.

## Purpose

This pipeline addresses critical challenges in modern agriculture by:
- Automating visual inspection of cabbage crops
- Detecting diseases and pest damage early
- Assessing crop quality and maturity
- Predicting harvest yields
- Reducing manual inspection labor
- Enabling data-driven farming decisions

## System Architecture

The pipeline consists of several interconnected stages:

```
Data Ingestion → Preprocessing → Feature Extraction → Analysis → Output
     ↓              ↓                  ↓               ↓          ↓
  Images         Cleaning          AI Models      Insights    Reports
  Videos       Augmentation       Detection      Metrics     Alerts
  Sensors      Normalization      Classification Predictions  API
```

## Features

### 1. Data Ingestion
- Support for multiple input sources:
  - Digital camera images
  - Drone aerial imagery
  - Time-lapse video feeds
  - IoT sensor data (temperature, humidity, soil conditions)
- Batch and real-time processing modes
- Automated data validation and quality checks

### 2. Image Preprocessing
- Image normalization and standardization
- Color correction and enhancement
- Noise reduction and filtering
- Image segmentation (separating cabbage from background)
- Data augmentation for training robustness

### 3. AI Model Components

#### Disease Detection
- Identifies common cabbage diseases:
  - Black rot
  - Clubroot
  - Downy mildew
  - Fusarium yellows
  - Alternaria leaf spot
- Confidence scoring for each detection
- Localization of affected areas

#### Quality Assessment
- Head size and shape analysis
- Density and compactness measurement
- Color uniformity evaluation
- Surface defect detection
- Grading according to market standards

#### Growth Stage Classification
- Seedling stage identification
- Vegetative growth monitoring
- Head formation tracking
- Maturity assessment
- Harvest readiness prediction

#### Yield Prediction
- Historical data analysis
- Weather pattern integration
- Growth rate calculations
- Expected harvest volume forecasting

### 4. Analysis and Insights
- Statistical summaries and trends
- Anomaly detection
- Comparative analysis across fields/plots
- Correlation with environmental factors
- Actionable recommendations

### 5. Output and Reporting
- Detailed analysis reports (PDF, HTML)
- Interactive dashboards
- Alert notifications for critical issues
- API endpoints for integration
- Export capabilities (CSV, JSON)

## Installation

### Prerequisites
```bash
Python 3.8+
CUDA-capable GPU (recommended)
8GB+ RAM
```

### Dependencies
```bash
# Core libraries
- TensorFlow / PyTorch
- OpenCV
- NumPy, Pandas
- Scikit-learn
- Pillow

# Visualization
- Matplotlib
- Seaborn
- Plotly

# Data handling
- SQLAlchemy
- boto3 (for cloud storage)

# Web framework (if using API)
- FastAPI / Flask
```

### Setup
```bash
# Clone repository
git clone https://github.com/Dronetdsp/cabbage-AI-analysis-pipeline.git
cd cabbage-AI-analysis-pipeline

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Download pre-trained models
python scripts/download_models.py

# Configure settings
cp config.example.yml config.yml
# Edit config.yml with your settings
```

## Usage

### Basic Pipeline Execution

```bash
# Analyze single image
python pipeline.py --input image.jpg --output results/

# Batch processing
python pipeline.py --input-dir data/images/ --output results/ --batch

# Real-time monitoring
python pipeline.py --mode stream --source camera --output results/
```

### Python API

```python
from cabbage_pipeline import CabbageAnalysisPipeline

# Initialize pipeline
pipeline = CabbageAnalysisPipeline(
    model_path='models/cabbage_detector.h5',
    config='config.yml'
)

# Analyze image
results = pipeline.analyze('path/to/cabbage_image.jpg')

# Access results
print(f"Quality Score: {results.quality_score}")
print(f"Diseases Detected: {results.diseases}")
print(f"Maturity Level: {results.maturity}")
print(f"Estimated Weight: {results.estimated_weight}")
```

### REST API

```bash
# Start API server
python api_server.py --port 8000

# Example API call
curl -X POST "http://localhost:8000/analyze" \
     -F "file=@cabbage.jpg" \
     -F "analysis_type=full"
```

## Pipeline Stages

### Stage 1: Data Loading
- Reads input images/videos
- Validates file formats
- Extracts metadata
- Organizes data for processing

### Stage 2: Preprocessing
- Resizes images to model input dimensions
- Applies color space transformations
- Performs background subtraction
- Normalizes pixel values

### Stage 3: Feature Extraction
- Runs images through CNN backbone
- Extracts deep features
- Computes hand-crafted features (color, texture, shape)
- Creates feature vectors

### Stage 4: Model Inference
- Disease classification
- Quality scoring
- Growth stage prediction
- Defect detection
- Yield estimation

### Stage 5: Post-processing
- Aggregates predictions
- Applies confidence thresholds
- Performs non-maximum suppression
- Generates bounding boxes and masks

### Stage 6: Output Generation
- Creates visualizations
- Generates reports
- Saves results to database
- Triggers alerts if needed

## Configuration

### config.yml Structure

```yaml
data:
  input_path: "data/input"
  output_path: "data/output"
  supported_formats: ["jpg", "jpeg", "png"]

models:
  disease_detector: "models/disease_detector.h5"
  quality_assessor: "models/quality_model.h5"
  yield_predictor: "models/yield_model.h5"

preprocessing:
  image_size: [512, 512]
  normalize: true
  augment: false

inference:
  batch_size: 16
  confidence_threshold: 0.7
  device: "cuda"  # or "cpu"

output:
  save_visualizations: true
  generate_reports: true
  export_format: "json"

alerts:
  enabled: true
  disease_threshold: 0.8
  email_notifications: true
```

## Model Training

### Dataset Requirements
- Minimum 1000+ labeled images per class
- Diverse lighting conditions
- Multiple growth stages represented
- Various cultivars included
- Balanced disease/healthy samples

### Training Pipeline

```bash
# Prepare dataset
python scripts/prepare_dataset.py --raw-data data/raw --output data/processed

# Train disease detection model
python train.py --model disease_detector --epochs 100 --batch-size 32

# Train quality assessment model
python train.py --model quality_assessor --epochs 50 --batch-size 16

# Evaluate models
python evaluate.py --model-dir models/ --test-data data/test
```

## Performance Metrics

Expected performance on validation data:
- Disease Detection Accuracy: >92%
- Quality Assessment MAE: <0.15 (on 0-1 scale)
- Growth Stage Classification: >88%
- Yield Prediction RMSE: <10% of actual yield

## Use Cases

1. **Commercial Farms**: Large-scale automated quality control and disease monitoring
2. **Research Institutions**: Crop breeding programs and agricultural research
3. **Smart Greenhouses**: Integrated monitoring in controlled environments
4. **Agricultural Consultants**: Data-driven advisory services
5. **Supply Chain**: Quality verification at collection points

## Limitations

- Performance depends on image quality and lighting conditions
- Requires significant training data for new disease types
- May need recalibration for different cabbage varieties
- Weather conditions can affect outdoor image capture
- GPU recommended for real-time processing

## Roadmap

- [ ] Support for additional cruciferous vegetables
- [ ] Mobile app for field deployment
- [ ] Integration with farm management systems
- [ ] Multi-spectral imaging support
- [ ] Automated drone integration
- [ ] Edge device deployment (Raspberry Pi, NVIDIA Jetson)
- [ ] Advanced phenotyping features

## Contributing

Contributions are welcome! Please follow these guidelines:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

### Development Setup
```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/

# Check code style
flake8 src/
black src/

# Run type checking
mypy src/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

- Documentation: [https://docs.cabbage-ai-pipeline.com](https://docs.cabbage-ai-pipeline.com)
- Issues: [GitHub Issues](https://github.com/Dronetdsp/cabbage-AI-analysis-pipeline/issues)
- Email: support@cabbage-ai-pipeline.com

## Acknowledgments

- Agricultural research institutions for dataset contributions
- Open-source computer vision community
- Farmers and agricultural experts for domain knowledge

## Citation

If you use this pipeline in your research, please cite:

```bibtex
@software{cabbage_ai_pipeline,
  title={Cabbage AI Analysis Pipeline},
  author={Your Name/Organization},
  year={2025},
  url={https://github.com/Dronetdsp/cabbage-AI-analysis-pipeline}
}
```

## Related Projects

- [PlantCV](https://plantcv.danforthcenter.org/) - Plant phenotyping tools
- [DeepLabCut](https://github.com/DeepLabCut/DeepLabCut) - Pose estimation
- [TorchVision](https://pytorch.org/vision/) - Computer vision models
- [AgML](https://github.com/Project-AgML/AgML) - Agricultural ML datasets

---

**Version**: 1.0.0
**Last Updated**: 2025-11-25
**Status**: Active Development
