# Release Notes - v1.0.0

**Release Date**: 2024-11-25

## 🎉 첫 번째 정식 릴리즈

Cabbage AI Analysis Pipeline v1.0.0은 CSV 파일을 통해 배치로 이미지를 분석할 수 있는 완전한 AI 분석 파이프라인입니다.

## ✨ 주요 기능

### 📊 CSV 기반 배치 처리
- CSV 파일로 여러 이미지를 한 번에 처리
- 자동 경로 검증 및 변환
- 상세한 검증 보고서

### 🖼️ 이미지 전처리
- 자동 리사이징 및 정규화
- 색상 보정 (CLAHE)
- 배경 제거
- 데이터 증강 (회전, 밝기 조정 등)

### 🤖 AI 모델 관리
- TensorFlow 및 PyTorch 지원
- 테스트용 Mock 모델
- 배치 예측
- 설정 파일 기반 모델 로딩

### 🌐 REST API
- FastAPI 기반 고성능 서버
- 대화형 API 문서 (Swagger UI)
- 비동기 작업 처리
- 실시간 상태 추적

### 🧪 완전한 테스트
- 모든 컴포넌트 단위 테스트
- API 통합 테스트
- pytest 기반 테스트 스위트

## 📦 포함된 컴포넌트

```
cabbage-AI-analysis-pipeline/
├── src/
│   ├── api/server.py              # REST API 서버
│   ├── models/model_loader.py     # 모델 로딩
│   ├── preprocessing/image_preprocessor.py  # 이미지 전처리
│   └── utils/csv_loader.py        # CSV 데이터 로더
├── tests/                         # 테스트 스위트
├── data/sample_input.csv          # 샘플 CSV
└── docs/                          # 문서
```

## 🚀 빠른 시작

### 1. 설치
```bash
pip install -r requirements.txt
```

### 2. API 서버 실행
```bash
python src/api/server.py
```

### 3. 브라우저에서 접속
```
http://localhost:8000/docs
```

### 4. CSV 파일 업로드
- Swagger UI에서 `/upload-csv` 엔드포인트 사용
- 분석 시작: `/analyze` 엔드포인트
- 결과 확인: `/results/{job_id}` 엔드포인트

## 📚 문서

- **[QUICKSTART.md](QUICKSTART.md)** - 5분 만에 시작하기
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - 상세 테스트 가이드 (한국어)
- **[cabbage-AI-analysis-pipeline.md](cabbage-AI-analysis-pipeline.md)** - 전체 시스템 문서
- **[CHANGELOG.md](CHANGELOG.md)** - 변경 이력

## 🔌 API 엔드포인트

| 메서드 | 엔드포인트 | 설명 |
|--------|-----------|------|
| POST | `/upload-csv` | CSV 파일 업로드 |
| POST | `/analyze` | 이미지 분석 시작 |
| GET | `/status/{job_id}` | 작업 상태 확인 |
| GET | `/results/{job_id}` | 분석 결과 조회 |
| GET | `/models` | 로드된 모델 목록 |
| POST | `/models/load` | 새 모델 로드 |
| POST | `/models/mock` | Mock 모델 생성 |
| GET | `/health` | 헬스 체크 |

## 💡 사용 예시

### Python 스크립트
```python
from src.utils.csv_loader import CSVDataLoader
from src.preprocessing.image_preprocessor import ImagePreprocessor
from src.models.model_loader import ModelLoader

# CSV 로드
loader = CSVDataLoader('data/my_images.csv')
summary = loader.get_summary()
print(f"처리할 이미지: {summary['valid_images']}개")

# 전처리
preprocessor = ImagePreprocessor(target_size=(512, 512))
images = preprocessor.preprocess_batch(loader.get_valid_images())

# 모델 로드 및 예측
model_loader = ModelLoader()
model_loader.create_mock_model('detector', (512, 512, 3))
predictions = model_loader.predict('detector', images)
```

### API 사용 (Python)
```python
import requests

# CSV 업로드
files = {'file': open('data/my_images.csv', 'rb')}
response = requests.post('http://localhost:8000/upload-csv', files=files)
file_id = response.json()['file_id']

# 분석 시작
response = requests.post(f'http://localhost:8000/analyze?file_id={file_id}')
job_id = response.json()['job_id']

# 결과 조회
response = requests.get(f'http://localhost:8000/results/{job_id}')
results = response.json()
```

### API 사용 (cURL)
```bash
# CSV 업로드
curl -X POST "http://localhost:8000/upload-csv" \
  -F "file=@data/sample_input.csv"

# 분석 시작
curl -X POST "http://localhost:8000/analyze?file_id=YOUR_FILE_ID"

# 상태 확인
curl "http://localhost:8000/status/YOUR_JOB_ID"
```

## 🧪 테스트 실행

```bash
# 모든 테스트
pytest tests/ -v

# 커버리지 포함
pytest tests/ --cov=src --cov-report=html

# 특정 테스트
pytest tests/test_csv_loader.py -v
```

## 📋 CSV 파일 형식

**필수 컬럼**: `image_path`

```csv
image_path,field_id,date,notes
images/cabbage1.jpg,1,2024-11-01,Healthy specimen
images/cabbage2.jpg,1,2024-11-02,Check for disease
images/cabbage3.jpg,2,2024-11-03,Ready to harvest
```

## 🔧 요구사항

- Python 3.8+
- OpenCV 4.x
- NumPy, Pandas
- TensorFlow 2.x 또는 PyTorch 2.x
- FastAPI
- pytest

## 🐛 알려진 이슈

현재 알려진 이슈 없음

## 🔜 다음 버전 계획

- [ ] 실제 AI 모델 통합
- [ ] 이미지 결과 시각화
- [ ] Excel 파일 지원
- [ ] 데이터베이스 연동
- [ ] Docker 이미지
- [ ] 성능 최적화

## 🤝 기여

Pull Request를 환영합니다!

## 📄 라이선스

MIT License

## 📞 지원

- **Issues**: https://github.com/Dronetdsp/cabbage-AI-analysis-pipeline/issues
- **Documentation**: 프로젝트 문서 참조

---

**Full Changelog**: https://github.com/Dronetdsp/cabbage-AI-analysis-pipeline/blob/main/CHANGELOG.md
