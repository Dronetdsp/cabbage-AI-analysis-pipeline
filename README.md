# Cabbage AI Analysis Pipeline

AI 기반 양배추 작물 분석 파이프라인 - CSV 파일을 업로드하여 이미지를 분석하는 엔드투엔드 시스템

## 개요

이 프로젝트는 컴퓨터 비전과 머신러닝을 활용하여 양배추 작물을 자동으로 분석하는 파이프라인입니다.

**주요 기능:**
- ✅ CSV 파일 기반 배치 이미지 처리
- ✅ 이미지 전처리 (리사이징, 정규화, 색상 보정)
- ✅ AI 모델 로딩 및 추론 (TensorFlow, PyTorch 지원)
- ✅ REST API 엔드포인트
- ✅ 질병 감지, 품질 평가, 성숙도 분류
- ✅ 완전한 테스트 스위트

## 빠른 시작

### 1. 설치
```bash
pip install -r requirements.txt
```

### 2. CSV 파일 준비
```csv
image_path,field_id,notes
images/cabbage1.jpg,1,Healthy
images/cabbage2.jpg,2,Check disease
```

### 3. 테스트 실행

**방법 A: API 서버**
```bash
python src/api/server.py
# 브라우저에서 http://localhost:8000/docs 열기
```

**방법 B: Python 스크립트**
```python
from src.utils.csv_loader import CSVDataLoader
from src.preprocessing.image_preprocessor import ImagePreprocessor

loader = CSVDataLoader('data/my_test.csv')
preprocessor = ImagePreprocessor()

for img in loader.get_valid_images():
    processed = preprocessor.preprocess(img['absolute_path'])
    print(f"처리 완료: {img['image_path']}")
```

**방법 C: 단위 테스트**
```bash
pytest tests/ -v
```

## 프로젝트 구조

```
cabbage-AI-analysis-pipeline/
├── src/
│   ├── api/              # FastAPI REST API
│   ├── models/           # 모델 로딩 및 추론
│   ├── preprocessing/    # 이미지 전처리
│   └── utils/            # CSV 로더 등 유틸리티
├── tests/                # 테스트 스위트
├── data/
│   ├── input/            # 입력 이미지
│   ├── output/           # 분석 결과
│   ├── uploads/          # CSV 업로드
│   └── sample_input.csv  # 샘플 CSV
├── QUICKSTART.md         # 빠른 시작 가이드
├── TESTING_GUIDE.md      # 상세 테스트 가이드 (한국어)
└── cabbage-AI-analysis-pipeline.md  # 전체 문서

```

## 문서

- **[QUICKSTART.md](QUICKSTART.md)** - 5분 만에 시작하기
- **[TESTING_GUIDE.md](TESTING_GUIDE.md)** - CSV 업로드 테스트 상세 가이드 (한국어)
- **[cabbage-AI-analysis-pipeline.md](cabbage-AI-analysis-pipeline.md)** - 전체 시스템 문서

## API 엔드포인트

- `POST /upload-csv` - CSV 파일 업로드
- `POST /analyze` - 이미지 분석 시작
- `GET /status/{job_id}` - 작업 상태 확인
- `GET /results/{job_id}` - 분석 결과 조회
- `GET /models` - 로드된 모델 목록
- `GET /health` - 헬스 체크

API 문서: http://localhost:8000/docs

## 테스트

```bash
# 모든 테스트 실행
pytest tests/ -v

# 커버리지 포함
pytest tests/ --cov=src

# 특정 테스트만
pytest tests/test_csv_loader.py -v
```

## 요구사항

- Python 3.8+
- OpenCV
- NumPy, Pandas
- TensorFlow 또는 PyTorch
- FastAPI
- pytest

## 라이선스

MIT License

## 기여

Pull Request를 환영합니다!

## 지원

- Issues: https://github.com/Dronetdsp/cabbage-AI-analysis-pipeline/issues
- Documentation: 프로젝트 루트의 마크다운 파일 참조