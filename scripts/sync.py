#!/usr/bin/env python3
"""
Notion 동기화 스크립트
- 데이터베이스 조회
- 페이지 목록 가져오기
- 변경사항 감지
"""

import os
import json
from datetime import datetime
from pathlib import Path

try:
    import requests
except ImportError:
    print("requests 패키지 필요: pip install requests")
    exit(1)

# 환경변수 로드
from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / "config" / ".env")

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_VERSION = "2022-06-28"

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION,
}


def search_pages(query: str = "") -> dict:
    """페이지 검색"""
    url = "https://api.notion.com/v1/search"
    payload = {"query": query, "page_size": 100}

    response = requests.post(url, headers=HEADERS, json=payload)
    return response.json()


def get_database(database_id: str) -> dict:
    """데이터베이스 조회"""
    url = f"https://api.notion.com/v1/databases/{database_id}/query"

    response = requests.post(url, headers=HEADERS)
    return response.json()


def get_page(page_id: str) -> dict:
    """페이지 조회"""
    url = f"https://api.notion.com/v1/pages/{page_id}"

    response = requests.get(url, headers=HEADERS)
    return response.json()


def get_blocks(block_id: str) -> dict:
    """블록 하위 조회"""
    url = f"https://api.notion.com/v1/blocks/{block_id}/children"

    response = requests.get(url, headers=HEADERS)
    return response.json()


def sync_all():
    """전체 동기화"""
    print("🔄 Notion 동기화 시작...")
    print(f"   시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    if not NOTION_API_KEY:
        print("❌ NOTION_API_KEY가 설정되지 않았습니다.")
        print("   config/.env 파일을 확인하세요.")
        return

    # 페이지 검색
    print("📄 페이지 검색 중...")
    result = search_pages()

    if "results" in result:
        pages = result["results"]
        print(f"   발견: {len(pages)} 개")

        for page in pages[:10]:  # 상위 10개만 표시
            title = "제목 없음"
            if page["object"] == "page":
                props = page.get("properties", {})
                for key, val in props.items():
                    if val.get("type") == "title":
                        title_arr = val.get("title", [])
                        if title_arr:
                            title = title_arr[0].get("plain_text", "제목 없음")
                        break
            elif page["object"] == "database":
                title_arr = page.get("title", [])
                if title_arr:
                    title = title_arr[0].get("plain_text", "데이터베이스")

            print(f"   - [{page['object']}] {title}")
    else:
        print(f"❌ 에러: {result.get('message', '알 수 없는 오류')}")

    print()
    print("✅ 동기화 완료!")


if __name__ == "__main__":
    sync_all()
