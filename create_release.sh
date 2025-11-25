#!/bin/bash

# GitHub Release 생성 스크립트
# v1.0.0 릴리즈를 GitHub에 생성합니다

# 설정
REPO_OWNER="Dronetdsp"
REPO_NAME="cabbage-AI-analysis-pipeline"
TAG_NAME="v1.0.0"
RELEASE_NAME="v1.0.0 - CSV Testing Infrastructure"

# 릴리즈 노트 읽기
RELEASE_BODY=$(cat RELEASE_NOTES.md)

# GitHub API URL
API_URL="https://api.github.com/repos/${REPO_OWNER}/${REPO_NAME}/releases"

echo "=========================================="
echo "GitHub Release 생성 준비"
echo "=========================================="
echo "Repository: ${REPO_OWNER}/${REPO_NAME}"
echo "Tag: ${TAG_NAME}"
echo "Release: ${RELEASE_NAME}"
echo "=========================================="
echo ""

# GitHub Personal Access Token이 필요합니다
if [ -z "$GITHUB_TOKEN" ]; then
    echo "❌ 오류: GITHUB_TOKEN 환경변수가 설정되지 않았습니다."
    echo ""
    echo "다음 단계를 따라주세요:"
    echo "1. GitHub에서 Personal Access Token 생성"
    echo "   https://github.com/settings/tokens"
    echo "2. 'repo' 권한 선택"
    echo "3. 토큰 생성 후 복사"
    echo "4. 다음 명령으로 설정:"
    echo "   export GITHUB_TOKEN='your_token_here'"
    echo "5. 이 스크립트 다시 실행"
    echo ""
    exit 1
fi

echo "✓ GitHub Token 확인됨"
echo ""

# JSON 페이로드 생성
json_payload=$(cat <<EOF
{
  "tag_name": "${TAG_NAME}",
  "name": "${RELEASE_NAME}",
  "body": $(echo "$RELEASE_BODY" | jq -Rs .),
  "draft": false,
  "prerelease": false
}
EOF
)

echo "릴리즈 생성 중..."
echo ""

# API 호출
response=$(curl -X POST \
  -H "Authorization: token ${GITHUB_TOKEN}" \
  -H "Accept: application/vnd.github.v3+json" \
  -H "Content-Type: application/json" \
  -d "$json_payload" \
  "${API_URL}" \
  -w "\n%{http_code}" \
  -s)

# HTTP 상태 코드 추출
http_code=$(echo "$response" | tail -n1)
response_body=$(echo "$response" | sed '$d')

if [ "$http_code" = "201" ]; then
    echo "=========================================="
    echo "✅ 릴리즈가 성공적으로 생성되었습니다!"
    echo "=========================================="
    echo ""

    # 릴리즈 URL 추출
    release_url=$(echo "$response_body" | jq -r '.html_url')
    echo "릴리즈 URL: ${release_url}"
    echo ""
    echo "브라우저에서 확인하세요:"
    echo "${release_url}"

elif [ "$http_code" = "422" ]; then
    echo "=========================================="
    echo "⚠️  릴리즈가 이미 존재합니다"
    echo "=========================================="
    echo ""
    echo "기존 릴리즈를 업데이트하거나 삭제 후 다시 시도하세요."
    echo "GitHub: https://github.com/${REPO_OWNER}/${REPO_NAME}/releases"

else
    echo "=========================================="
    echo "❌ 릴리즈 생성 실패"
    echo "=========================================="
    echo "HTTP 상태 코드: ${http_code}"
    echo ""
    echo "응답:"
    echo "$response_body" | jq . 2>/dev/null || echo "$response_body"
fi

echo ""
echo "=========================================="
