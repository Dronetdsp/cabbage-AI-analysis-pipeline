# Testing Guide - Cabbage AI Analysis Pipeline

이 가이드는 CSV 파일을 업로드하여 파이프라인을 테스트하는 방법을 설명합니다.

## 목차
1. [설치](#설치)
2. [CSV 파일 준비](#csv-파일-준비)
3. [테스트 방법](#테스트-방법)
4. [API 사용](#api-사용)
5. [문제 해결](#문제-해결)

---

## 설치

### 1. 의존성 설치

```bash
# 가상환경 생성 (권장)
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# 패키지 설치
pip install -r requirements.txt
```

### 2. 디렉토리 구조 확인

```
cabbage-AI-analysis-pipeline/
├── data/
│   ├── input/          # 이미지 파일 위치
│   ├── output/         # 분석 결과 저장
│   ├── uploads/        # CSV 업로드 위치
│   └── sample_input.csv  # 샘플 CSV 템플릿
├── src/
│   ├── api/
│   ├── models/
│   ├── preprocessing/
│   └── utils/
└── tests/
```

---

## CSV 파일 준비

### CSV 파일 형식

CSV 파일은 **반드시** `image_path` 컬럼을 포함해야 합니다:

```csv
image_path,field_id,date,notes
images/cabbage_001.jpg,1,2024-11-01,Healthy
images/cabbage_002.jpg,1,2024-11-02,Check for disease
images/cabbage_003.jpg,2,2024-11-03,Ready to harvest
```

### 필수 컬럼
- **image_path**: 이미지 파일 경로 (상대 경로 또는 절대 경로)

### 선택 컬럼 (예시)
- field_id: 밭 구역 ID
- date: 촬영 날짜
- location: 위치
- notes: 메모
- label: 라벨 (healthy, diseased 등)

### 샘플 CSV 사용

프로젝트에 포함된 샘플 CSV를 사용할 수 있습니다:

```bash
cp data/sample_input.csv data/my_test.csv
# 편집기로 my_test.csv를 열어 실제 이미지 경로로 수정
```

---

## 테스트 방법

### 방법 1: 단위 테스트 실행

```bash
# 모든 테스트 실행
pytest tests/ -v

# 특정 테스트만 실행
pytest tests/test_csv_loader.py -v
pytest tests/test_preprocessor.py -v
pytest tests/test_model_loader.py -v
pytest tests/test_api.py -v

# 커버리지 포함
pytest tests/ --cov=src --cov-report=html
```

### 방법 2: Python 스크립트로 테스트

#### CSV 로더 테스트

```python
from src.utils.csv_loader import CSVDataLoader

# CSV 파일 로드
loader = CSVDataLoader('data/sample_input.csv', base_path='.')
loader.load()

# 요약 정보 확인
summary = loader.get_summary()
print(f"전체 레코드: {summary['total_records']}")
print(f"유효한 이미지: {summary['valid_images']}")
print(f"잘못된 이미지: {summary['invalid_images']}")

# 유효한 이미지 목록
valid_images = loader.get_valid_images()
for img in valid_images:
    print(f"이미지: {img['image_path']}")
```

#### 이미지 전처리 테스트

```python
from src.preprocessing.image_preprocessor import ImagePreprocessor
import matplotlib.pyplot as plt

# 전처리기 초기화
preprocessor = ImagePreprocessor(
    target_size=(512, 512),
    normalize=True
)

# 이미지 전처리
image_path = 'path/to/your/cabbage.jpg'
processed = preprocessor.preprocess(image_path)

print(f"처리된 이미지 크기: {processed.shape}")
print(f"픽셀 범위: [{processed.min():.2f}, {processed.max():.2f}]")

# 시각화
plt.imshow(processed)
plt.title('전처리된 이미지')
plt.show()
```

#### 모델 로더 테스트

```python
from src.models.model_loader import ModelLoader
import numpy as np

# 모델 로더 초기화
loader = ModelLoader(model_dir='data/models')

# 테스트용 Mock 모델 생성
loader.create_mock_model(
    model_name='disease_detector',
    input_shape=(512, 512, 3),
    num_classes=5
)

# 테스트 입력 생성
test_input = np.random.rand(1, 512, 512, 3).astype(np.float32)

# 예측 실행
predictions = loader.predict('disease_detector', test_input)
print(f"예측 결과: {predictions}")
```

---

## API 사용

### 1. API 서버 시작

```bash
python src/api/server.py
```

서버가 시작되면:
- API 문서: http://localhost:8000/docs
- 대체 문서: http://localhost:8000/redoc

### 2. CSV 파일 업로드 (curl 사용)

```bash
# CSV 파일 업로드
curl -X POST "http://localhost:8000/upload-csv" \
  -F "file=@data/sample_input.csv"
```

응답 예시:
```json
{
  "file_id": "abc123-def456-ghi789",
  "filename": "sample_input.csv",
  "validation": {
    "valid": true,
    "columns": ["image_path", "field_id", "date", "notes"],
    "row_count": 5,
    "error": null
  }
}
```

### 3. 분석 시작

```bash
# file_id는 업로드 응답에서 받은 값 사용
curl -X POST "http://localhost:8000/analyze?file_id=abc123-def456-ghi789"
```

응답 예시:
```json
{
  "job_id": "xyz789-uvw456-rst123",
  "status": "queued",
  "summary": {
    "total_records": 5,
    "valid_images": 3,
    "invalid_images": 2
  }
}
```

### 4. 상태 확인

```bash
curl -X GET "http://localhost:8000/status/xyz789-uvw456-rst123"
```

### 5. 결과 조회

```bash
curl -X GET "http://localhost:8000/results/xyz789-uvw456-rst123"
```

### 6. Python으로 API 사용

```python
import requests

# 1. CSV 업로드
with open('data/sample_input.csv', 'rb') as f:
    files = {'file': ('sample.csv', f, 'text/csv')}
    response = requests.post('http://localhost:8000/upload-csv', files=files)
    file_id = response.json()['file_id']

print(f"파일 업로드 완료: {file_id}")

# 2. 분석 시작
response = requests.post(f'http://localhost:8000/analyze?file_id={file_id}')
job_id = response.json()['job_id']

print(f"분석 시작: {job_id}")

# 3. 상태 확인
import time

while True:
    response = requests.get(f'http://localhost:8000/status/{job_id}')
    status = response.json()
    print(f"진행 상황: {status['progress']}")

    if status['status'] in ['completed', 'completed_with_errors']:
        break

    time.sleep(2)

# 4. 결과 조회
response = requests.get(f'http://localhost:8000/results/{job_id}')
results = response.json()

print(f"\n분석 완료!")
print(f"처리된 이미지: {results['processed_images']}/{results['total_images']}")
print(f"결과: {len(results['results'])}개")
print(f"에러: {len(results['errors'])}개")
```

---

## 문제 해결

### 1. CSV 파일 검증 실패

**문제**: "CSV must contain 'image_path' column" 에러

**해결**:
- CSV 파일에 `image_path` 컬럼이 있는지 확인
- 컬럼 이름의 철자와 대소문자 확인
- CSV 파일이 올바른 형식인지 확인

### 2. 이미지 파일을 찾을 수 없음

**문제**: "Image not found" 에러

**해결**:
```python
# 절대 경로 사용
loader = CSVDataLoader('data/sample_input.csv', base_path='/full/path/to/images')

# 또는 CSV에 절대 경로 작성
# image_path
# /home/user/images/cabbage1.jpg
```

### 3. 모듈 import 에러

**문제**: "ModuleNotFoundError" 에러

**해결**:
```bash
# requirements.txt 재설치
pip install -r requirements.txt --force-reinstall

# 또는 개별 설치
pip install numpy pandas opencv-python pillow
```

### 4. TensorFlow/PyTorch 설치 문제

**TensorFlow**:
```bash
# CPU 버전
pip install tensorflow

# GPU 버전 (CUDA 필요)
pip install tensorflow-gpu
```

**PyTorch**:
```bash
# CPU 버전
pip install torch torchvision --index-url https://download.pytorch.org/whl/cpu

# GPU 버전 (공식 사이트에서 명령어 확인)
# https://pytorch.org/get-started/locally/
```

### 5. API 서버 포트 충돌

**문제**: 포트 8000이 이미 사용 중

**해결**:
```bash
# 다른 포트 사용
uvicorn src.api.server:app --host 0.0.0.0 --port 8080
```

---

## 고급 테스트

### 배치 처리 성능 테스트

```python
import time
from src.preprocessing.image_preprocessor import ImagePreprocessor

preprocessor = ImagePreprocessor()

# 이미지 경로 목록
image_paths = [f'path/to/image_{i}.jpg' for i in range(100)]

# 처리 시간 측정
start_time = time.time()
batch = preprocessor.preprocess_batch(image_paths)
elapsed = time.time() - start_time

print(f"100개 이미지 처리 시간: {elapsed:.2f}초")
print(f"이미지당 평균: {elapsed/100:.3f}초")
```

### 모델 추론 성능 테스트

```python
import time
import numpy as np
from src.models.model_loader import ModelLoader

loader = ModelLoader()
loader.create_mock_model('test_model', (512, 512, 3), num_classes=5)

# 배치 입력
batch_sizes = [1, 4, 8, 16, 32]

for batch_size in batch_sizes:
    test_input = np.random.rand(batch_size, 512, 512, 3).astype(np.float32)

    start_time = time.time()
    predictions = loader.predict('test_model', test_input)
    elapsed = time.time() - start_time

    print(f"배치 크기 {batch_size}: {elapsed:.4f}초 ({elapsed/batch_size:.4f}초/이미지)")
```

---

## 다음 단계

1. **실제 모델 학습**: `cabbage-AI-analysis-pipeline.md` 참조
2. **프로덕션 배포**: Docker 컨테이너 사용
3. **성능 최적화**: GPU 사용, 배치 크기 조정
4. **모니터링**: 로깅 및 메트릭 추가

---

## 지원

문제가 발생하면:
1. GitHub Issues: https://github.com/Dronetdsp/cabbage-AI-analysis-pipeline/issues
2. 문서: `cabbage-AI-analysis-pipeline.md` 참조

