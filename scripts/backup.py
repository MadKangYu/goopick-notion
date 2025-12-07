#!/usr/bin/env python3
"""
Notion 백업 스크립트
- 모든 페이지 JSON 백업
- 일자별 백업 폴더 생성
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

from dotenv import load_dotenv
load_dotenv(Path(__file__).parent.parent / "config" / ".env")

NOTION_API_KEY = os.getenv("NOTION_API_KEY")
NOTION_VERSION = "2022-06-28"
BACKUP_DIR = Path(__file__).parent.parent / "backups"

HEADERS = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": NOTION_VERSION,
}


def search_all() -> list:
    """모든 페이지/데이터베이스 검색"""
    url = "https://api.notion.com/v1/search"
    all_results = []
    has_more = True
    start_cursor = None

    while has_more:
        payload = {"page_size": 100}
        if start_cursor:
            payload["start_cursor"] = start_cursor

        response = requests.post(url, headers=HEADERS, json=payload)
        data = response.json()

        if "results" in data:
            all_results.extend(data["results"])
            has_more = data.get("has_more", False)
            start_cursor = data.get("next_cursor")
        else:
            break

    return all_results


def get_page_content(page_id: str) -> dict:
    """페이지 전체 내용 가져오기"""
    # 페이지 메타데이터
    page_url = f"https://api.notion.com/v1/pages/{page_id}"
    page_resp = requests.get(page_url, headers=HEADERS)
    page_data = page_resp.json()

    # 블록 내용
    blocks_url = f"https://api.notion.com/v1/blocks/{page_id}/children"
    blocks_resp = requests.get(blocks_url, headers=HEADERS)
    blocks_data = blocks_resp.json()

    return {
        "page": page_data,
        "blocks": blocks_data.get("results", [])
    }


def backup():
    """전체 백업 실행"""
    print("💾 Notion 백업 시작...")
    print(f"   시간: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()

    if not NOTION_API_KEY:
        print("❌ NOTION_API_KEY가 설정되지 않았습니다.")
        return

    # 백업 폴더 생성
    today = datetime.now().strftime("%Y-%m-%d")
    backup_path = BACKUP_DIR / today
    backup_path.mkdir(parents=True, exist_ok=True)

    # 모든 항목 검색
    print("🔍 페이지 검색 중...")
    items = search_all()
    print(f"   발견: {len(items)} 개")
    print()

    # 각 항목 백업
    backed_up = 0
    for item in items:
        item_id = item["id"]
        item_type = item["object"]

        try:
            if item_type == "page":
                content = get_page_content(item_id)
                filename = f"page_{item_id.replace('-', '')}.json"
            else:
                content = item
                filename = f"db_{item_id.replace('-', '')}.json"

            filepath = backup_path / filename
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(content, f, ensure_ascii=False, indent=2)

            backed_up += 1
            print(f"   ✓ {filename}")

        except Exception as e:
            print(f"   ✗ {item_id}: {e}")

    print()
    print(f"✅ 백업 완료! ({backed_up}/{len(items)})")
    print(f"   위치: {backup_path}")


if __name__ == "__main__":
    backup()
