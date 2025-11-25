# GitHub Release 생성 가이드

v1.0.0 릴리즈를 GitHub에 만드는 방법입니다.

## 🎯 현재 상태

✅ 모든 코드 커밋 완료
✅ Git 태그 생성 완료 (`v1.0.0`)
✅ 태그 GitHub에 푸시 완료
✅ 릴리즈 문서 작성 완료

**이제 GitHub Release만 만들면 됩니다!**

---

## 방법 1: 자동 스크립트 (제일 빠름!)

### 사전 준비

1. **GitHub Personal Access Token 생성**
   - https://github.com/settings/tokens 접속
   - "Generate new token" → "Generate new token (classic)" 클릭
   - Note: "Release Creation" (아무 이름)
   - Expiration: 7 days (또는 원하는 기간)
   - **'repo' 전체 체크** ✅
   - "Generate token" 클릭
   - **토큰 복사** (다시 볼 수 없으니 저장!)

### 실행

```bash
# 1. 토큰 설정 (위에서 복사한 토큰 사용)
export GITHUB_TOKEN='ghp_your_token_here'

# 2. 스크립트 실행
./create_release.sh
```

성공하면 릴리즈 URL이 출력됩니다!

---

## 방법 2: GitHub 웹에서 수동 생성 (제일 쉬움!)

### 단계별 가이드

1. **GitHub 저장소로 이동**
   ```
   https://github.com/Dronetdsp/cabbage-AI-analysis-pipeline
   ```

2. **Releases 페이지로 이동**
   - 우측 사이드바에서 "Releases" 클릭
   - 또는 직접 이동: https://github.com/Dronetdsp/cabbage-AI-analysis-pipeline/releases

3. **"Draft a new release" 클릭**

4. **릴리즈 정보 입력**

   **Choose a tag:**
   ```
   v1.0.0
   ```
   (드롭다운에서 선택 - 이미 존재함)

   **Release title:**
   ```
   v1.0.0 - CSV Testing Infrastructure
   ```

   **Describe this release:**

   `RELEASE_NOTES.md` 파일의 전체 내용을 복사해서 붙여넣기

   또는 아래 내용 복사:

```markdown
# 🎉 첫 번째 정식 릴리즈

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
- 데이터 증강

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

## 🚀 빠른 시작

```bash
# 설치
pip install -r requirements.txt

# API 서버 실행
python src/api/server.py

# 브라우저에서
http://localhost:8000/docs
```

## 📚 문서

- **QUICKSTART.md** - 5분 만에 시작하기
- **TESTING_GUIDE.md** - 상세 테스트 가이드 (한국어)
- **cabbage-AI-analysis-pipeline.md** - 전체 시스템 문서

## 🔌 API 엔드포인트

- `POST /upload-csv` - CSV 파일 업로드
- `POST /analyze` - 이미지 분석 시작
- `GET /status/{job_id}` - 작업 상태 확인
- `GET /results/{job_id}` - 분석 결과 조회
- `GET /models` - 로드된 모델 목록
- `GET /health` - 헬스 체크

**Full Changelog**: https://github.com/Dronetdsp/cabbage-AI-analysis-pipeline/blob/main/CHANGELOG.md
```

5. **옵션 설정**
   - ✅ "Set as the latest release" 체크
   - ⬜ "Set as a pre-release" 체크 안 함

6. **"Publish release" 클릭**

완료! 🎉

---

## 방법 3: GitHub CLI 사용 (설치된 경우)

```bash
# GitHub CLI 설치 확인
gh --version

# 릴리즈 생성
gh release create v1.0.0 \
  --title "v1.0.0 - CSV Testing Infrastructure" \
  --notes-file RELEASE_NOTES.md \
  --repo Dronetdsp/cabbage-AI-analysis-pipeline
```

---

## ✅ 릴리즈 생성 후 확인사항

릴리즈가 생성되면 다음을 확인하세요:

1. **릴리즈 페이지 확인**
   ```
   https://github.com/Dronetdsp/cabbage-AI-analysis-pipeline/releases/tag/v1.0.0
   ```

2. **자동 생성되는 것들**
   - Source code (zip)
   - Source code (tar.gz)

3. **릴리즈 배지 (선택)**

   README에 추가할 수 있는 배지:
   ```markdown
   ![Release](https://img.shields.io/github/v/release/Dronetdsp/cabbage-AI-analysis-pipeline)
   ```

---

## 🔧 문제 해결

### "Release already exists" 에러

기존 릴리즈를 수정하려면:
1. Releases 페이지에서 v1.0.0 찾기
2. 우측 "Edit" 버튼 클릭
3. 내용 수정 후 "Update release"

### 태그가 없다는 에러

```bash
# 태그 존재 확인
git tag -l

# 태그 푸시
git push origin v1.0.0
```

---

## 📝 요약

**가장 쉬운 방법**: 방법 2 (웹에서 수동 생성)
- 5분이면 완료
- GitHub 계정만 있으면 됨
- 토큰 불필요

**가장 빠른 방법**: 방법 1 (자동 스크립트)
- 1분이면 완료
- GitHub Token 필요
- 명령어 한 줄

선택해서 진행하세요! 🚀
