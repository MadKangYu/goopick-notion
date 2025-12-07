# goopick-notion

Notion API 연동 및 자동화 저장소

## 기능

- Notion 데이터베이스 동기화
- 페이지 백업 및 내보내기
- Claude ↔ Notion 연동
- 자동화 워크플로우

## 구조

```
goopick-notion/
├── scripts/
│   ├── sync.py           # Notion 동기화
│   ├── backup.py         # 페이지 백업
│   └── export.py         # 마크다운 내보내기
├── config/
│   └── .env.example      # 환경변수 예시
├── backups/              # 백업 데이터
└── exports/              # 내보내기 결과
```

## 설정

### 1. Notion Integration 생성
1. https://www.notion.so/my-integrations 접속
2. "New integration" 클릭
3. API 키 복사

### 2. 환경변수 설정
```bash
cp config/.env.example config/.env
# NOTION_API_KEY 입력
```

### 3. 데이터베이스 연결
- Notion에서 데이터베이스 공유 → Integration 추가

## 사용법

```bash
# 동기화
python scripts/sync.py

# 백업
python scripts/backup.py

# 마크다운 내보내기
python scripts/export.py
```

## 연동

- **goopick-orchestra**: 통합 관리
- **goopick-claude**: Claude 작업물 연동
- **goopick-vault**: Obsidian 동기화
