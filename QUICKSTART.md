# Quick Start Guide

CSV 파일을 업로드하여 빠르게 테스트하는 방법입니다.

## 1. 설치 (2분)

```bash
# 의존성 설치
pip install -r requirements.txt
```

## 2. CSV 파일 준비

샘플 CSV 파일을 복사하여 수정하세요:

```bash
cp data/sample_input.csv data/my_test.csv
```

CSV 형식:
```csv
image_path,field_id,notes
images/cabbage1.jpg,1,Healthy
images/cabbage2.jpg,1,Check disease
```

**중요**: `image_path` 컬럼은 필수입니다!

## 3. 테스트 방법 선택

### 옵션 A: API 서버 사용 (추천)

```bash
# 1. 서버 시작
python src/api/server.py

# 2. 브라우저에서 http://localhost:8000/docs 열기
# 3. "upload-csv" 엔드포인트에서 CSV 파일 업로드
# 4. "analyze" 엔드포인트에서 분석 시작
```

### 옵션 B: Python 스크립트

```python
from src.utils.csv_loader import CSVDataLoader
from src.preprocessing.image_preprocessor import ImagePreprocessor

# CSV 로드
loader = CSVDataLoader('data/my_test.csv')
summary = loader.get_summary()
print(f"유효한 이미지: {summary['valid_images']}개")

# 이미지 전처리
preprocessor = ImagePreprocessor()
for img in loader.get_valid_images():
    processed = preprocessor.preprocess(img['absolute_path'])
    print(f"처리 완료: {img['image_path']}")
```

### 옵션 C: 단위 테스트

```bash
pytest tests/ -v
```

## 4. 결과 확인

- API: http://localhost:8000/results/{job_id}
- 파일: `data/output/` 디렉토리 확인

## 문제 해결

### CSV 에러
```
"CSV must contain 'image_path' column"
```
→ CSV 파일에 `image_path` 컬럼 추가

### 이미지 없음
```
"Image not found"
```
→ CSV의 경로가 올바른지 확인

## 다음 단계

자세한 내용은 다음 문서를 참조하세요:
- **상세 테스트**: `TESTING_GUIDE.md`
- **전체 문서**: `cabbage-AI-analysis-pipeline.md`
